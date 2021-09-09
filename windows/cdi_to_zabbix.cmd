@echo off
taskkill /F /IM DISKINFO64.exe
taskkill /F /IM DISKINFO32.exe

start "no title" "C:\Program Files\CrystalDiskInfo\DiskInfo64.exe" /Copy

rem wait for CDI write DiskInfo.txt
timeout /T 10 /NOBREAK > nul

python C:\usr\src\crystaldiskinfo_to_zabbix\crystaldiskinfo_to_zabbix.py