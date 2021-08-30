from pyzabbix import ZabbixMetric, ZabbixSender

import interpriters

import json
import logging
import subprocess
import struct
import time
from datetime import datetime

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

  if SMARTCTL_SCAN_CMD[0] == 'sudo':
    logger.info("Asking your password by sudo") 

  scan = subprocess.run(SMARTCTL_SCAN_CMD, encoding='utf-8', stdout=subprocess.PIPE)
  
  # logger.debug(scan.stdout)
  result = json.loads(scan.stdout)
  #logger.debug(result)
  return result


def exec_smartctl_device_info(device_name):

  run_cmd = SMARTCTL_DETAIL_CMD.copy()
  run_cmd.append(device_name)

  logger.debug(run_cmd)
  device_info = subprocess.run(run_cmd, encoding='utf-8', stdout=subprocess.PIPE)
  
  #logger.debug(device_info.stdout)
  result = json.loads(device_info.stdout)
  #logger.debug(result)
  return result


def send_discovery(full_result):

  logger.info("Send discovery to zabbix")

  # drive list /dev/sda /dev/sdb ...
  drives = []
  for drv in full_result["scan"]["devices"]:
    drives.append(drv["name"])

  discovery_result = []
  for drive in drives:
    detail = full_result[drive]
    discovery_result.append({KEY_NAME: drive, DISK_NAME: detail["model_name"]})

  data = {"request": "sender data", "data":[]}
  valueStr = json.dumps({"data": discovery_result})
  one_data = {"host": ZABBIX_HOST, "key": DISCOVERY_KEY, "value": f"{valueStr}"}
  data["data"].append(one_data)

  text = json.dumps(data)

  send_to_zabbix_raw(text)

  return None


def get_detail(device):

     # sender data
    metrics = []
    for d in device:
      key = f"smartmontools.diskname[{d['KEY']}]"
      logger.debug(key)
      #metrics.append(ZabbixMetric(ZABBIX_HOST, key, d["VALUE"]))

    send_to_zabbix(metrics)

    return None


def receive(sock, count):

    buf = b''

    while len(buf) < count:
        chunk = sock.recv(count - len(buf))
        if not chunk:
            break
        buf += chunk

    return buf
    

def send_to_zabbix(dictdata):
  data = json.dumps(dictdata)
  logger.debug(f"data length is {len(data)}")
  send_to_zabbix_raw(data)


def send_to_zabbix_raw(data):
  import socket

  data_len = struct.pack('<L', len(data))
  packet = b'ZBXD\x01' + data_len + b'\x00\x00\x00\x00' +  data.encode('utf-8')

  connection = socket.socket(socket.AF_INET)
  connection.settimeout(15)
  
  try:
      connection.connect((ZABBIX_SERVER, ZABBIX_PORT))
      logger.debug("Connected")
      connection.sendall(packet)
      logger.debug("Data sent")
  except socket.timeout:
      logger.error('Sending failed: Timeout')
      connection.close()
      raise socket.timeout
  except socket.error as err:
      logger.warning('Sending failed: %s', getattr(err, 'msg', str(err)))
      connection.close()
      raise err

  response_header = receive(connection, 13)
  # logger.debug('Response header: %s', response_header)

  if (not response_header.startswith(b'ZBXD\x01') or
          len(response_header) != 13):
      logger.info('Zabbix return not valid response.')
      result = False
  else:
      response_len = struct.unpack('<Q', response_header[5:])[0]
      response_body = connection.recv(response_len)
      result = json.loads(response_body.decode("utf-8"))
      logger.info('Data received: %s', result)

  try:
      connection.close()
  except socket.error:
      pass

  return result


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

  full_result = {"scan": scan_result}

  for device in scan_result["devices"]:
    dev = device["name"]
    logger.info(f"Checking device {dev}")
    device_info = exec_smartctl_device_info(device["name"])

    interpriter = find_interpriter(device_info)

    full_result[dev] = interpriter(device_info)

  send_discovery(full_result)
  

    

