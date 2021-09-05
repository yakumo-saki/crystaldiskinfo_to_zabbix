import os
from os.path import join, dirname

# load_dotenvはファイルが存在しなくても素通りする
# load_dotenvはすでにexportされている環境変数を上書きしない
from dotenv import load_dotenv
load_dotenv(join(dirname(__file__), '.env'))

# 環境変数を読む。 
ZABBIX_SERVER = os.environ.get('ZABBIX_SERVER', None)
ZABBIX_PORT = int(os.environ.get('ZABBIX_PORT', "10051"))
ZABBIX_HOST = os.environ.get('ZABBIX_HOST', None)
LOG_LEVEL = os.environ.get('LOG_LEVEL', "DEBUG")

# 以下はZabbixテンプレートと整合性を取る必要がある

#  
LINUX_SMARTCTL_SCAN_CMD = ['sudo', 'smartctl', '--json', '--scan']
LINUX_SMARTCTL_DETAIL_CMD = ['sudo', 'smartctl', '--json', '-a']

# 
WIN_SMARTCTL_SCAN_CMD = ['smartctl', '--json', '--scan']
WIN_SMARTCTL_DETAIL_CMD = ['smartctl', '--json', '-a']
