import logging
import json
import struct

logger = logging.getLogger(__name__)


def receive(sock, count):

    buf = b''

    while len(buf) < count:
        chunk = sock.recv(count - len(buf))
        if not chunk:
            break
        buf += chunk

    return buf
 

"""zabbixにデータを送信します
data = json.dumpsしたテキスト
"""
def send_to_zabbix_raw(zabbix_server, zabbix_port, json_text):
  import socket

  data_len = struct.pack('<L', len(json_text))
  packet = b'ZBXD\x01' + data_len + b'\x00\x00\x00\x00' +  json_text.encode('utf-8')

  connection = socket.socket(socket.AF_INET)
  connection.settimeout(15)
  
  try:
      connection.connect((zabbix_server, zabbix_port))
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
