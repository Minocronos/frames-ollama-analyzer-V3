@echo off
REM ========================================
REM Export du projet pour transport
REM ========================================

REM Remonter à la racine du projet
pushd "%~dp0.."

echo.
echo ========================================
echo  Export du projet
echo ========================================
echo.

REM Nom du fichier ZIP
set EXPORT_NAME=frames-analyzer-V3-export.zip

echo Preparation de l'export...
echo Fichier: %EXPORT_NAME%
echo.

REM Supprimer l'ancien ZIP s'il existe
if exist %EXPORT_NAME% del %EXPORT_NAME%

echo Creation du ZIP (cela peut prendre quelques secondes)...

REM Créer le ZIP en préservant la structure (exclusion des dossiers lourds/inutiles)
powershell -Command "$exclude = @('.venv', '__pycache__', '.git', 'saved_collections', '%EXPORT_NAME%'); $items = Get-ChildItem -Path . | Where-Object { $exclude -notcontains $_.Name }; Compress-Archive -Path $items.FullName -DestinationPath '%EXPORT_NAME%' -Force"

if errorlevel 1 (
    echo.
    echo [ERROR] Impossible de creer le ZIP
    echo Verifiez que PowerShell est disponible
    pause
    exit /b 1
)

if exist %EXPORT_NAME% (
    echo.
    echo ========================================
    echo  Export termine!
    echo ========================================
    echo.
    echo Fichier cree: %EXPORT_NAME%
    
    REM Afficher la taille
    for %%A in (%EXPORT_NAME%) do echo Taille: %%~zA octets
    
    echo.
    echo Ce fichier contient tout le necessaire pour
    echo transporter l'application sur une autre machine.
    echo.
    echo Sur la nouvelle machine:
    echo   1. Dezipper le fichier
    echo   2. Executer scripts\setup.bat
    echo   3. Executer run.bat
    echo.
) else (
    echo.
    echo [ERROR] Le fichier ZIP n'a pas ete cree
    echo.
)

pause
