from pyzabbix import ZabbixMetric, ZabbixSender

import interpriters
import json
import logging
import subprocess
from pprint import pprint

import config as cfg

import modules.zabbix_parsed as zbx_parsed
import modules.zabbix_smart as zbx_smart

logging.basicConfig(encoding='utf-8', level=logging.INFO)
logger = logging.getLogger(__name__)

def exec_smartctl_scan():

  cmd = None

  import platform
  platform = platform.system()
  if platform == 'Windows':
    cmd = cfg.WIN_SMARTCTL_SCAN_CMD.copy()
  else:
    cmd = cfg.LINUX_SMARTCTL_SCAN_CMD.copy()

  if cmd[0] == 'sudo':
    logger.info("Asking your password by sudo") 

  scan = subprocess.run(cmd, encoding='utf-8', stdout=subprocess.PIPE)
  
  # logger.debug(scan.stdout)
  result = json.loads(scan.stdout)
  #logger.debug(result)
  return result


def exec_smartctl_device_info(device_name):

  run_cmd = None

  import platform
  platform = platform.system()
  if platform == 'Windows':
    run_cmd = cfg.WIN_SMARTCTL_DETAIL_CMD.copy()
  else:
    run_cmd = cfg.LINUX_SMARTCTL_DETAIL_CMD.copy()

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

    zbx_parsed.send_to_zabbix(metrics)

    return None


def find_interpriter(device_info):
    # strict match
    for intp in interpriters.ALL:
      if (intp.isTargetDeviceType(device_info) and intp.isTargetStrict(device_info)):
        return intp

    # loose match
    for intp in interpriters.ALL:
      if (intp.isTargetDeviceType(device_info) and intp.isTargetLoose(device_info)):
        return intp

    # basic
    for intp in interpriters.BASIC:
      logger.warn(f"No matching interpriters => {dev} {device_info['model_name']}, using basic interprites instead.")
      if (intp.isTargetDeviceType(device_info)):
        return intp

    logger.debug(f"No interpriters => {dev} {device_info['model_name']}")
    raise "No interpriters"


if __name__ == '__main__':

  logger.info("START")

  # scan_resultだけでdiscoveryを送信したいが、model_name等情報が足りない
  scan_result = exec_smartctl_scan()
   
  full_results = {}
  parsed_results = {}

  for device in scan_result["devices"]:
    dev = device["name"]
    logger.info(f"Checking device {dev}")
    device_info = exec_smartctl_device_info(device["name"])
    full_results[dev] = device_info

    interpriter = find_interpriter(device_info)

    parsed_results[dev] = interpriter.parse(device_info)

  # パース成功したデータを扱う
  zbx_parsed.send_device_discovery(parsed_results)
  zbx_parsed.send_parsed_data(parsed_results)

  # SMART全データを送信する
  zbx_smart.send_attribute_discovery(full_results)


  logger.info("END")
