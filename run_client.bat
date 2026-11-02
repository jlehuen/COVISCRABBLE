@echo off
cd /d "%~dp0"
python main_client.py -fr -host localhost -port 1234
pause
