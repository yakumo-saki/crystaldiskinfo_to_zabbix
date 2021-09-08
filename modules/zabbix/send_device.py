import json
import logging
import config as cfg

from modules.const import Keys, DeviceKey, AttrKey

from modules.zabbix.sender import send_to_zabbix

logger = logging.getLogger(__name__)


"""zabbixにDevice LLDデータを送信します。
result = {"/dev/sda": {"model": EXAMPLE SSD 250, "POWER_CYCLE": 123 ...}}
"""
def send_device_discovery(result):

  logger.info("Sending device discovery to zabbix")

  discovery_result = []
  for drive in result:
    detail = result[drive]
    discovery_result.append({DeviceKey.KEY_NAME: drive, DeviceKey.DISK_NAME: detail[Keys.DISK_MODEL]})

  data = {"request": "sender data", "data":[]}
  valueStr = json.dumps({"data": discovery_result})
  one_data = {"host": cfg.ZABBIX_HOST, "key": DeviceKey.KEY, "value": f"{valueStr}"}
  data["data"].append(one_data)

  send_to_zabbix(data)

  return None


"""interpriterで解釈出来たデータを送信する。
smartctlが解釈してくれたもの＋独自に解釈したデータ
data = {
    "host1": {
        "item1": 1234,
        "item2": "value"
    },
    "host2": {
        "item1": 5678,
        "item2": "value"
    }
}
"""
def send_parsed_data(data):
  logger.info("Send data to zabbix")

  # results = {"smartmontools.version": "7.2"}
  # for dev in data:
  #   detail = data[dev]
    
  #   for key in detail:
  #     if detail[key]:
  #       zbx_key = Keys.zabbix_key(key, dev)
  #       results[zbx_key] = detail[key]

  # sender_data = {"request": "sender data", "data": {cfg.ZABBIX_HOST: results}}

  results = []
  for dev in data:
    detail = data[dev]  # /dev/sda
    
    for key in detail:
      if detail[key] != None:  # key exists ?
        results.append({
          "host": cfg.ZABBIX_HOST,
          "key": Keys.zabbix_key(key, dev),
          "value": detail[key]
        })

  sender_data = {"request": "sender data", "data": results}
  #valueStr = json.dumps({"data": discovery_result})
  # print(json.dumps(sender_data, indent=2))

  send_to_zabbix(sender_data)

  return None
