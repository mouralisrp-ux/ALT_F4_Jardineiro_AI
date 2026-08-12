import sys, os, json, time, threading, traceback
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QListWidget, QMessageBox, QSpinBox, QGroupBox
)
from PySide6.QtCore import QObject, Signal
from pynput import keyboard, mouse

APP_DIR = Path(os.getenv("LOCALAPPDATA", Path.home())) / "ALT_F4_Jardineiro_AI"
DATA = APP_DIR / "sequences"
DATA.mkdir(parents=True, exist_ok=True)

class Recorder(QObject):
    finished = Signal(list)
    status = Signal(str)

    def __init__(self):
        super().__init__()
        self.events = []
        self.running = False

    def start(self):
        if self.running:
            return
        self.events = []
        self.t0 = time.perf_counter()
        self.running = True
        self.kl = keyboard.Listener(on_press=self.kp, on_release=self.kr)
        self.ml = mouse.Listener(on_move=self.mm, on_click=self.mc)
        self.kl.start()
        self.ml.start()
        self.status.emit("A gravar... F9 termina e guarda.")

    def t(self):
        return round(time.perf_counter() - self.t0, 4)

    def key(self, k):
        try:
            return k.char
        except Exception:
            return str(k)

    def kp(self, k):
        if self.running:
            self.events.append({"t": self.t(), "type": "key_down", "key": self.key(k)})

    def kr(self, k):
        if self.running:
            self.events.append({"t": self.t(), "type": "key_up", "key": self.key(k)})

    def mm(self, x, y):
        if self.running:
            self.events.append({"t": self.t(), "type": "mouse_move", "x": x, "y": y})

    def mc(self, x, y, b, pressed):
        if self.running:
            self.events.append({
                "t": self.t(), "type": "mouse_click", "x": x, "y": y,
                "button": str(b), "pressed": pressed
            })

    def stop(self):
        if not self.running:
            return
        self.running = False
        try:
            self.kl.stop()
            self.ml.stop()
        except Exception:
            pass
        self.finished.emit(self.events)
        self.status.emit(f"Gravação terminada: {len(self.events)} eventos.")

class Player(QObject):
    status = Signal(str)
    finished = Signal(str)

    def __init__(self):
        super().__init__()
        self.stop_flag = False

    def stop(self):
        self.stop_flag = True

    def run(self, events, reps):
        def job():
            kb = keyboard.Controller()
            ms = mouse.Controller()
            self.stop_flag = False

            try:
                for r in range(reps):
                    self.status.emit(f"Execução {r + 1}/{reps}")
                    last = 0
                    for e in events:
                        if self.stop_flag:
                            self.finished.emit("Execução interrompida.")
                            return

                        time.sleep(max(0, e["t"] - last))
                        last = e["t"]

                        try:
                            if e["type"] == "key_down":
                                kb.press(self.convkey(e["key"]))
                            elif e["type"] == "key_up":
                                kb.release(self.convkey(e["key"]))
                            elif e["type"] == "mouse_move":
                                ms.position = (e["x"], e["y"])
                            elif e["type"] == "mouse_click":
                                b = getattr(mouse.Button, e["button"].split(".")[-1])
                                (ms.press if e["pressed"] else ms.release)(b)
                        except Exception:
                            # Ignore one malformed event and continue.
                            pass

                self.finished.emit("Execução concluída.")
            except Exception as exc:
                self.finished.emit(f"Erro: {exc}")

        threading.Thread(target=job, daemon=True).start()

    def convkey(self, s):
        if s.startswith("Key."):
            return getattr(keyboard.Key, s[4:], keyboard.Key.esc)
        return s

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ALT F4 Jardineiro AI — V2")
        self.resize(760, 540)

        self.rec = Recorder()
        self.player = Player()
        self.build()

        self.rec.finished.connect(self.saved)
        self.rec.status.connect(self.status.setText)
        self.player.status.connect(self.status.setText)
        self.player.finished.connect(self.status.setText)

        self.hot = keyboard.GlobalHotKeys({
            "<f8>": self.startrec,
            "<f9>": self.stoprec,
            "<f10>": self.stopplay
        })
        self.hot.start()

    def build(self):
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<h2>ALT F4 Jardineiro AI — V2</h2>"))
        layout.addWidget(QLabel("Grava teclado/rato, guarda sequências e repete-as automaticamente."))

        group = QGroupBox("Configuração")
        row = QHBoxLayout(group)

        row.addWidget(QLabel("Nome:"))
        self.name = QLineEdit("jardineiro_01")
        row.addWidget(self.name)

        row.addWidget(QLabel("Repetições:"))
        self.reps = QSpinBox()
        self.reps.setRange(1, 10000)
        self.reps.setValue(10)
        row.addWidget(self.reps)
        layout.addWidget(group)

        buttons = QHBoxLayout()
        for text, fn in [
            ("F8 — Gravar", self.startrec),
            ("F9 — Parar e guardar", self.stoprec),
            ("F10 — PARAR", self.stopplay),
        ]:
            b = QPushButton(text)
            b.clicked.connect(fn)
            buttons.addWidget(b)
        layout.addLayout(buttons)

        self.list = QListWidget()
        layout.addWidget(self.list)

        run = QPushButton("Executar sequência selecionada")
        run.clicked.connect(self.play)
        layout.addWidget(run)

        self.status = QLabel("Pronto. F8 grava • F9 guarda • F10 interrompe.")
        layout.addWidget(self.status)

        self.load()

    def load(self):
        self.list.clear()
        for p in sorted(DATA.glob("*.json")):
            self.list.addItem(p.stem)

    def startrec(self):
        self.rec.start()

    def stoprec(self):
        self.rec.stop()

    def saved(self, events):
        name = self.name.text().strip() or f"sequencia_{int(time.time())}"
        safe = "".join(c for c in name if c.isalnum() or c in " _-").strip()
        if not safe:
            safe = f"sequencia_{int(time.time())}"

        path = DATA / f"{safe}.json"
        path.write_text(
            json.dumps({"name": safe, "events": events}, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
        self.load()
        self.status.setText(f"Guardado: {safe}")

    def play(self):
        item = self.list.currentItem()
        if not item:
            QMessageBox.warning(self, "Atenção", "Seleciona uma sequência.")
            return

        try:
            data = json.loads((DATA / f"{item.text()}.json").read_text(encoding="utf-8"))
            self.player.run(data.get("events", []), self.reps.value())
        except Exception as exc:
            QMessageBox.critical(self, "Erro", f"Não foi possível abrir a sequência:\n{exc}")

    def stopplay(self):
        self.player.stop()
        self.status.setText("A parar...")

    def closeEvent(self, event):
        try:
            self.rec.stop()
            self.player.stop()
            self.hot.stop()
        except Exception:
            pass
        event.accept()

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        w = App()
        w.show()
        sys.exit(app.exec())
    except Exception:
        traceback.print_exc()
        raise
