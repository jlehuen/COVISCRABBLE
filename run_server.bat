@echo off
cd /d "%~dp0"
set PYTHONPATH=%~dp0src;%PYTHONPATH%
python src\main_server.py -fr -port 1234 -data database
pause
