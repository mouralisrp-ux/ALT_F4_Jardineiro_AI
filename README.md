# ALT F4 Jardineiro AI — V2

Ferramenta de gravação e reprodução automática de ações de teclado e rato para Windows.

## Funcionalidades

- ✅ Gravação de teclado e rato
- ✅ Reprodução de sequências gravadas
- ✅ Atalhos globais (F8, F9, F10)
- ✅ Gestão de sequências
- ✅ Interface simples e intuitiva
- ✅ Executável Windows standalone

## Atalhos

- **F8**: Iniciar/Parar gravação
- **F9**: Guardar sequência
- **F10**: Parar/Cancelar execução

## Como usar

### Instalação (Desenvolvimento)

```bash
git clone https://github.com/mouralisrp-ux/ALT_F4_Jardineiro_AI.git
cd ALT_F4_Jardineiro_AI
pip install -r requirements.txt
python app.py
```

### Gerar Executável

1. Ir a **Actions** no repositório
2. Selecionar **Build ALT F4 Jardineiro AI**
3. Clicar **Run workflow**
4. Após conclusão, descarregar o artifact `ALT_F4_Jardineiro_AI-Windows`

### Usar o Executável

Após gerar o executável, executar diretamente:

```bash
ALT_F4_Jardineiro_AI.exe
```

Não requer Python instalado.

## Estrutura de Ficheiros

```
├── app.py                        # Aplicação principal
├── requirements.txt              # Dependências Python
├── ALT_F4_Jardineiro_AI.spec    # Configuração PyInstaller
├── .github/workflows/build.yml   # GitHub Actions workflow
└── README.md                     # Este ficheiro
```

## Dados Guardados

As sequências são guardadas em:
- Windows: `%LOCALAPPDATA%\ALT_F4_Jardineiro_AI\sequences`

Formato: JSON com eventos e timestamps.

## Requisitos

- Python 3.9+ (para desenvolvimento)
- Windows 10+
- Permissões para aceder a teclado e rato

## Tecnologias

- **PySide6**: Interface gráfica
- **pynput**: Captura de teclado e rato
- **PyInstaller**: Geração de executável
- **GitHub Actions**: Build automático

## Licença

MIT
