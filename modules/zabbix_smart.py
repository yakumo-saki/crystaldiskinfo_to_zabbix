import json
import logging
import config as cfg

from modules.const import Keys, AttrKey

from modules.zabbix_sender import send_to_zabbix

logger = logging.getLogger(__name__)


"""zabbixにS.M.A.R.T Attribute LLDデータを送信します。
Attribute LLDとは要するにSMART値すべて
"""
def send_attribute_discovery(result):

  logger.info("Sending attribute discovery to zabbix")

  discovery_result = []
  for device in result:
    detail = result[device]

    discovery = {AttrKey.DEV_NAME: device, AttrKey.DISK_NAME: detail["model_name"]}
    if ("ata_smart_attributes" in detail):
      discovery_result = create_attribute_list_non_nvme(discovery, detail["ata_smart_attributes"])
    elif ("nvme_smart_health_information_log" in detail):
      discovery_result = create_attribute_list_nvme(discovery, detail["nvme_smart_health_information_log"])
    
  data = {"request": "sender data", "data":[]}
  valueStr = json.dumps({"data": discovery_result})
  one_data = {"host": cfg.ZABBIX_HOST, "key": AttrKey.KEY, "value": f"{valueStr}"}
  data["data"].append(one_data)

  send_to_zabbix(data)

  return None


def create_attribute_list_non_nvme(discovery_base, smart_attributes):
  import copy 

  result = []
  for attr in smart_attributes["table"]:
    discovery = copy.deepcopy(discovery_base)

    # non NVMeの場合、 Unknown Attributeがあり得るので、SMART ID を名前の先頭につけておく
    discovery[AttrKey.ATTR_NAME] = "{0} {1}".format(attr["id"], attr["name"])
    discovery[AttrKey.ATTR_ID] = attr["id"]
    result.append(discovery)

  return result


def create_attribute_list_nvme(discovery_base, smart_attributes):
  import copy 

  result = []
  for key in smart_attributes:
    discovery = copy.deepcopy(discovery_base)

    if key == "temperature_sensors":
      for val, idx in smart_attributes["temperature_sensors"]:
        discovery[AttrKey.ATTR_NAME] = f"temperature_sensors{idx}"
        discovery[AttrKey.ATTR_ID] = f"temperature_sensors{idx}"
    else:
      discovery[AttrKey.ATTR_NAME] = key
      discovery[AttrKey.ATTR_ID] = key
    result.append(discovery)

  return result


def send_smart_data(data):
  logger.info("Send S.M.A.R.T data to zabbix")

  results = []
  for dev in data:
    detail = data[dev]  # /dev/sda
    
    if ("ata_smart_attributes" in detail):
      results = create_value_list_non_nvme(dev, detail["ata_smart_attributes"])
    elif ("nvme_smart_health_information_log" in detail):
      results = create_value_list_nvme(dev, detail["nvme_smart_health_information_log"])

  sender_data = {"request": "sender data", "data": results}
  #valueStr = json.dumps({"data": discovery_result})
  # print(json.dumps(sender_data, indent=2))

  send_to_zabbix(sender_data)

  return None


def create_value_list_non_nvme(dev, smart_attributes):
  results = []
  for attr in smart_attributes["table"]:

    keyvalue = {
      AttrKey.RAWVALUE_KEY.format(dev, attr["id"]): attr["raw"]["value"],
      AttrKey.VALUE_KEY.format(dev, attr["id"]): attr["value"],
      AttrKey.WORST_KEY.format(dev, attr["id"]): attr["worst"]
    }

    for k,v in keyvalue.items():
      results.append({"host": cfg.ZABBIX_HOST, "key": k, "value": v})

  return results


def create_value_list_nvme(dev, smart_attributes):
  results = []
  for key in smart_attributes:

    # NVMe にはthreshouldやworstはなく、valueだけ
    if key == "temperature_sensors":
      for val, idx in smart_attributes["temperature_sensors"]:
        key = AttrKey.VALUE_KEY.format(dev, f"temperature_sensors{idx}")
        results.append({"host": cfg.ZABBIX_HOST, "key": key, "value": val})
    else:
      key = AttrKey.VALUE_KEY.format(dev, key)
      results.append({"host": cfg.ZABBIX_HOST, "key": key, "value": val})

  return results
