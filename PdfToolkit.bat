@echo off

cd /d "%~dp0"

if not exist venv (
    echo Creating virtual environment...
    py -m venv venv
)

REM Activate the virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Install required packages
if exist requirements.txt (
    echo Installing requirements...
    pip install -r requirements.txt --disable-pip-version-check
)

REM Run the Python script
echo Running main.py...
start pythonw main.py

REM Deactivate the virtual environment
deactivate