@echo off
setlocal
echo ==========================================
echo       Installation de PMCLI v2.0...
echo ==========================================

:: Verification Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERREUR] Python n'a pas ete trouve.
    pause
    exit /b 1
)

:: Appel de l'installeur PowerShell pour la gestion du PATH
echo [INFO] Lancement de l'installation automatique...
powershell -ExecutionPolicy Bypass -File "%~dp0install.ps1"

endlocal
