@echo off
taskkill /F /IM DISKINFO64.exe
taskkill /F /IM DISKINFO32.exe

del "C:\Program Files\CrystalDiskInfo\DiskInfo.txt"
start "no title" "C:\Program Files\CrystalDiskInfo\DiskInfo64.exe" /Copy

echo "Wait for CrystalDiskInfo write DiskInfo.txt"
timeout /T 10 /NOBREAK > nul

python C:\usr\src\crystaldiskinfo_to_zabbix\crystaldiskinfo_to_zabbix.py