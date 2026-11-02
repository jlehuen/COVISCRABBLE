@echo off
cd /d "%~dp0"
set PYTHONPATH=%~dp0src;%PYTHONPATH%
python src\main_client.py -fr -host localhost -port 1234
pause
