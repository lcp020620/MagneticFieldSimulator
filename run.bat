@echo off
if not exist "venv" (
    echo Generating Vircual environment...
    python -m venv venv
)

call venv\Scripts\activate
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo [error] There was an issue during library installation. 
    echo Check your python version or internet connection.
    pause
)
python app.py

exit