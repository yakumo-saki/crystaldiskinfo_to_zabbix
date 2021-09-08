import json
import logging
import config as cfg

from modules.const import Keys, DeviceKey, AttrKey

from modules.zabbix.sender import send_to_zabbix

logger = logging.getLogger(__name__)


"""zabbixにDevice LLDデータを送信します。
"""
def send_device_discovery(data):

  logger.info("Sending device discovery to zabbix")

  diskDetails = data["diskDetail"]

  discovery_result = []
  for disk in diskDetails:
    discovery_result.append({
      DeviceKey.DISK_KEY: disk[Keys.KEY], 
      DeviceKey.DISK_NAME: disk[Keys.NAME]
    })


  data = {"request": "sender data", "data":[]}
  valueStr = json.dumps({"data": discovery_result})

  logger.debug(json.dumps(discovery_result, indent=2, ensure_ascii=False))

  discoveryData = {
    "host": cfg.ZABBIX_HOST,
    "key": DeviceKey.ZBX_KEY,
    "value": f"{valueStr}"
  }
  data["data"].append(discoveryData)

  send_to_zabbix(data)

  return None


def send_device_data(data):
  logger.info("Send data to zabbix")

  diskDetails = data["diskDetail"]

  NO_SEND = [Keys.ID, Keys.KEY, Keys.NAME, Keys.INTERFACE, Keys.SMART]

  results = []
  for disk in diskDetails:
    for key in disk.keys():
      if key in NO_SEND: continue

      if disk[key] != None:  # Noneを送っても意味がないので送らない
        results.append({
          "host": cfg.ZABBIX_HOST,
          "key": Keys.zabbix_key(key, disk[Keys.KEY]),
          "value": disk[key]
        })

  sender_data = {"request": "sender data", "data": results}

  send_to_zabbix(sender_data)

  return None
