import json
import logging
import config as cfg

from modules.const import Keys

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

"""
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
def send_data(data):
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
  print(json.dumps(sender_data, indent=2))

  send_to_zabbix(sender_data)

  return None
