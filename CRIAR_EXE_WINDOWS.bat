@echo off
setlocal
title ALT F4 Jardineiro AI - Criar EXE
echo.
echo ALT F4 Jardineiro AI
echo A criar a aplicacao Windows...
echo.

where py >nul 2>&1
if %errorlevel%==0 (set "PY=py") else (set "PY=python")

%PY% -m pip install --upgrade pip
%PY% -m pip install -r requirements.txt
if errorlevel 1 goto :error

%PY% -m pip install --upgrade pyinstaller
if errorlevel 1 goto :error

%PY% -m PyInstaller --noconfirm --clean ALT_F4_Jardineiro_AI.spec
if errorlevel 1 goto :error

echo.
echo ==========================================
echo CONCLUIDO!
echo O EXE esta em:
echo dist\ALT_F4_Jardineiro_AI.exe
echo ==========================================
pause
exit /b 0

:error
echo.
echo ERRO durante a criacao do EXE.
pause
exit /b 1
