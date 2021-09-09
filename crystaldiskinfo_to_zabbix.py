import json
import logging
from pprint import pprint

import config as cfg

import modules.parser.cdi_parser as parser
import modules.zabbix.send_device as send_device
import modules.zabbix.send_smart as send_smart

logger = logging.getLogger(__name__)


if __name__ == '__main__':

    if (cfg.LOG_LEVEL.upper() == "ERROR"):
        logging.basicConfig(encoding='utf-8', level=logging.ERROR)
    elif (cfg.LOG_LEVEL.upper() == "WARN"):
        logging.basicConfig(encoding='utf-8', level=logging.WARN)
    elif (cfg.LOG_LEVEL.upper() == "INFO"):
        logging.basicConfig(encoding='utf-8', level=logging.INFO)
    elif (cfg.LOG_LEVEL.upper() == "DEBUG"):
        logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
    else:
        logging.basicConfig(encoding='utf-8', level=logging.INFO)

    logger.debug("START")

    result = parser.parse(cfg.DISKINFO_TXT)

    # for debug purpose, export parsed.json if configured
    if (cfg.PARSED_JSON != ""):
        logger.debug(f"Exporting parsed.json: {cfg.PARSED_JSON}")
        with open(cfg.PARSED_JSON, 'w', encoding='UTF-8') as f:
            f.write(json.dumps(result, indent=2, ensure_ascii=False))


    # CDIの解釈データを送る
    send_device.send_device_discovery(result)
    send_device.send_device_data(result)

    # SMART全データを送信する
    send_smart.send_attribute_discovery(result)
    send_smart.send_smart_data(result)

    logger.debug("END")
