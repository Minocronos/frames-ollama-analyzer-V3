@echo off
REM ========================================
REM Verification de l'environnement
REM ========================================

REM Remonter à la racine du projet
pushd "%~dp0.."

echo.
echo ========================================
echo  Verification de l'environnement
echo ========================================
echo.

echo [Python]
python --version 2>nul
if errorlevel 1 (
    echo   [X] Python non trouve
    set PYTHON_OK=0
) else (
    echo   [OK] Python installe
    set PYTHON_OK=1
)

echo.
echo [uv]
uv --version 2>nul
if errorlevel 1 (
    echo   [X] uv non installe
    set UV_OK=0
) else (
    echo   [OK] uv installe
    set UV_OK=1
)

echo.
echo [Environnement virtuel]
if exist .venv (
    echo   [OK] .venv existe
    set VENV_OK=1
) else (
    echo   [X] .venv n'existe pas
    set VENV_OK=0
)

echo.
echo [Dependances]
if exist requirements.txt (
    echo   [OK] requirements.txt present
) else (
    echo   [X] requirements.txt manquant
)

if exist pyproject.toml (
    echo   [OK] pyproject.toml present
) else (
    echo   [X] pyproject.toml manquant
)

echo.
echo ========================================
echo  Resume
echo ========================================

if %PYTHON_OK%==0 (
    echo [ACTION REQUISE] Installez Python 3.11+
)

if %UV_OK%==0 (
    echo [INFO] uv sera installe automatiquement par setup.bat
)

if %VENV_OK%==0 (
    echo [ACTION REQUISE] Executez scripts\setup.bat pour creer l'environnement
) else (
    echo [OK] Environnement pret! Utilisez run.bat pour lancer l'app
)

echo.
pause
