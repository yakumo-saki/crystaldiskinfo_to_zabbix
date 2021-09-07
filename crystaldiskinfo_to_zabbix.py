from pyzabbix import ZabbixMetric, ZabbixSender

import logging
from pprint import pprint

import config as cfg

import modules.parser.cdi_parser as parser

logger = logging.getLogger(__name__)


if __name__ == '__main__':

    if (cfg.LOG_LEVEL.upper() == "ERROR"):
        logging.basicConfig(encoding='utf-8', level=logging.ERROR)
    elif (cfg.LOG_LEVEL.upper() == "WARN"):
        logging.basicConfig(encoding='utf-8', level=logging.WARN)
    elif (cfg.LOG_LEVEL.upper() == "INFO"):
        logging.basicConfig(encoding='utf-8', level=logging.INFO)
    else:
        logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

    logger.info("START")

    parser.parse(cfg.DISKINFO_TXT)

    # SMART全データを送信する
    #zbx_smart.send_attribute_discovery(full_results)
    #zbx_smart.send_smart_data(full_results)

    logger.info("END")
