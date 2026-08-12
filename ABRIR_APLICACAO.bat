@echo off
if exist "dist\ALT_F4_Jardineiro_AI.exe" (
    start "" "dist\ALT_F4_Jardineiro_AI.exe"
) else (
    echo Ainda nao existe o EXE.
    echo Execute CRIAR_EXE_WINDOWS.bat primeiro.
    pause
)
