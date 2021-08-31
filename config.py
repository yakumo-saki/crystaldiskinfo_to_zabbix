# change for your environment.
ZABBIX_SERVER = "10.1.0.10"
ZABBIX_PORT = 10051

ZABBIX_HOST = 'test'
KEY_NAME = '{#KEYNAME}'
DISK_NAME = '{#DISKNAME}'
DISCOVERY_KEY = 'smartmontools.discovery'
ITEM_KEY = 'smartmontools.disk.smart[{}]'

SMARTCTL_SCAN_CMD = ['sudo', 'smartctl', '--json', '--scan']
SMARTCTL_DETAIL_CMD = ['sudo', 'smartctl', '--json', '-a']
