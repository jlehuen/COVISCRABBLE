@echo off
cd /d "%~dp0"
python main_server.py -fr -port 1234 -data database
pause
