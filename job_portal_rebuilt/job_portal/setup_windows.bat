@echo off
setlocal
cd /d %~dp0
if not exist .venv (
  echo Creating virtual environment...
  py -m venv .venv
)
call .venv\Scripts\activate.bat
echo Installing dependencies...
python -m pip install -r requirements.txt
echo Applying migrations and creating demo jobs...
python manage.py migrate
python manage.py seed_demo
echo.
echo JobNest is ready.
echo Start with: python manage.py runserver
pause
