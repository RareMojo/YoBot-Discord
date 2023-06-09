@echo off
echo Setting up YoBot...

echo Creating virtual environment...
python -m venv venv
call venv\Scripts\activate.bat

echo Upgrading pip...
python -m pip install --upgrade pip --progress-bar on

echo Installing dependencies...
python -m pip install -r requirements.txt --progress-bar on

echo Starting YoBot...
python src\main.py
pause
