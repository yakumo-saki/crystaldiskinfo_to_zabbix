from pyzabbix import ZabbixMetric, ZabbixSender

import interpriters
import json
import logging
import subprocess
from pprint import pprint

import config as cfg

import lib.zabbix as zabbix


POWER_CYCLE = "power_cycle"
ROTATION_RATE = "rotation_rate"
POWER_ON_HOURS = "power_on_hours"
TEMPERATURE = "temperature"
DISK_MODEL = "model"
DISK_TYPE = "type"
DISK_ROTATION_RATE = "rotation_rate"
SSD_BYTES_WRITTEN = "ssd.bytes_written"
SSD_LIFESPAN = "ssd.lifespan"

RESULT_BASE = {
  POWER_CYCLE: "", ROTATION_RATE: "", POWER_ON_HOURS: "",


}

logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
logger = logging.getLogger(__name__)

def exec_smartctl_scan():

  if cfg.SMARTCTL_SCAN_CMD[0] == 'sudo':
    logger.info("Asking your password by sudo") 

  scan = subprocess.run(cfg.SMARTCTL_SCAN_CMD, encoding='utf-8', stdout=subprocess.PIPE)
  
  # logger.debug(scan.stdout)
  result = json.loads(scan.stdout)
  #logger.debug(result)
  return result


def exec_smartctl_device_info(device_name):

  run_cmd = cfg.SMARTCTL_DETAIL_CMD.copy()
  run_cmd.append(device_name)

  logger.debug(run_cmd)
  device_info = subprocess.run(run_cmd, encoding='utf-8', stdout=subprocess.PIPE)
  
  #logger.debug(device_info.stdout)
  result = json.loads(device_info.stdout)
  #logger.debug(result)
  return result


def get_detail(device):

     # sender data
    metrics = []
    for d in device:
      key = f"smartmontools.diskname[{d['KEY']}]"
      logger.debugf("get_detail {key}")
      #metrics.append(ZabbixMetric(ZABBIX_HOST, key, d["VALUE"]))

    zabbix.send_to_zabbix(metrics)

    return None


def find_interpriter(device_info):
    info = None
    for intp in interpriters.ALL:
      if (intp.isTargetStrict(device_info)):
        return intp

    for intp in interpriters.ALL:
      if (intp.isTargetLoose(device_info)):
        return intp

    logger.debug(f"No interpriters => {dev} {device_info['model_name']}")
    return interpriters.BASIC


if __name__ == '__main__':

  logger.info("START")

  # scan_resultだけでdiscoveryを送信したいが、model_name等情報が足りない
  scan_result = exec_smartctl_scan()
  parsed_results = {}

  for device in scan_result["devices"]:
    dev = device["name"]
    logger.info(f"Checking device {dev}")
    device_info = exec_smartctl_device_info(device["name"])

    interpriter = find_interpriter(device_info)

    parsed_results[dev] = interpriter.parse(device_info)

  logger.debug(parsed_results)
  zabbix.send_discovery(parsed_results)

  logger.info("END")
    

