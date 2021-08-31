import json
import logging
import config as cfg

from const import Keys

from modules.zabbix_sender import send_to_zabbix_raw

logger = logging.getLogger(__name__)

def send_to_zabbix(dictdata):
  data = json.dumps(dictdata)
  logger.debug(f"data length is {len(data)}")
  send_to_zabbix_raw(cfg.ZABBIX_SERVER, cfg.ZABBIX_PORT ,data)


"""zabbixにLLDデータを送信します。
result = {"/dev/sda": {"model": EXAMPLE SSD 250, "POWER_CYCLE": 123 ...}}
"""
def send_discovery(result):

  logger.info("Send discovery to zabbix")

  discovery_result = []
  for drive in result:
    detail = result[drive]
    discovery_result.append({cfg.KEY_NAME: drive, cfg.DISK_NAME: detail[Keys.DISK_MODEL]})

  data = {"request": "sender data", "data":[]}
  valueStr = json.dumps({"data": discovery_result})
  one_data = {"host": cfg.ZABBIX_HOST, "key": cfg.DISCOVERY_KEY, "value": f"{valueStr}"}
  data["data"].append(one_data)

  send_to_zabbix(data)

  return None