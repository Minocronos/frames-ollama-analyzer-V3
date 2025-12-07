@echo off
REM ========================================
REM Frames Analyser - Setup Script
REM ========================================

REM Remonter à la racine du projet
pushd "%~dp0.."

echo.
echo ========================================
echo  Frames Analyser - Installation
echo ========================================
echo.

REM Check Python version
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python n'est pas installe ou pas dans le PATH
    echo Installez Python 3.11+ depuis https://www.python.org/
    pause
    exit /b 1
)

echo [1/4] Verification de Python...
python --version

REM Check if uv is installed
echo.
echo [2/4] Verification de uv...
uv --version >nul 2>&1
if errorlevel 1 (
    echo uv n'est pas installe. Installation de uv...
    pip install uv
    if errorlevel 1 (
        echo [ERROR] Impossible d'installer uv
        pause
        exit /b 1
    )
)
uv --version

REM Create virtual environment with uv
echo.
echo [3/4] Creation de l'environnement virtuel...
if exist .venv (
    echo Environnement virtuel existant detecte
    choice /C YN /M "Voulez-vous le recreer"
    if errorlevel 2 goto skip_venv
    echo Suppression de l'ancien environnement...
    rmdir /s /q .venv
)

uv venv
if errorlevel 1 (
    echo [ERROR] Impossible de creer l'environnement virtuel
    pause
    exit /b 1
)

:skip_venv
REM Install dependencies
echo.
echo [4/4] Installation des dependances...
uv pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Impossible d'installer les dependances
    pause
    exit /b 1
)

echo.
echo ========================================
echo  Installation terminee avec succes!
echo ========================================
echo.
echo Pour lancer l'application, executez:
echo   run.bat
echo.
pause
