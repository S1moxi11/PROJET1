@echo off

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Veuillez installer python pour continuer : https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe

    pause
    exit /b
)

REM Check if the virtual environment exists
if not exist venv (
    echo Création de l'environnement virtuel
    python -m venv venv
)

echo Activation de l'environnement virtuel...
call venv\Scripts\activate

echo Installation des modules nécessaires...
pip install -r requirements.txt

echo Lancement du jeu...
python projet/VERSION1.py

echo Désactivation de l'environnement virtuel...
deactivate

pause
