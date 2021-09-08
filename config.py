import os
from os.path import join, dirname
from distutils.util import strtobool

# load_dotenvはファイルが存在しなくても素通りする
# load_dotenvはすでにexportされている環境変数を上書きしない
from dotenv import load_dotenv
load_dotenv(join(dirname(__file__), '.env'))

# 環境変数を読む。 
DISKINFO_TXT = os.environ.get('DISKINFO_TXT', None)
ZABBIX_SERVER = os.environ.get('ZABBIX_SERVER', None)
ZABBIX_PORT = int(os.environ.get('ZABBIX_PORT', "10051"))
ZABBIX_HOST = os.environ.get('ZABBIX_HOST', None)

LOG_LEVEL = os.environ.get('LOG_LEVEL', "INFO")

PARSED_JSON = os.environ.get('PARSED_JSON', "")

ABORT_WHEN_HIDE_SN = strtobool(os.environ.get('ABORT_WHEN_HIDE_SN', "False"))

SEND_SMART_VALUE=strtobool(os.environ.get('SEND_SMART_VALUE', "True"))
SEND_SMART_WORST=strtobool(os.environ.get('SEND_SMART_WORST', "True"))
SEND_SMART_THRESHOULD=strtobool(os.environ.get('SEND_SMART_THRESHOULD', "True"))
