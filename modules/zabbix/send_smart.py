import json
import logging
import config as cfg

from modules.const import Keys, AttrKey

from modules.zabbix.sender import send_to_zabbix

logger = logging.getLogger(__name__)


"""zabbixにS.M.A.R.T Attribute LLDデータを送信します。
Attribute LLDとは要するにSMART値すべて
"""
def send_attribute_discovery(data):

    logger.info("Sending attribute discovery to zabbix")

    discovery_result = []
    for device in data[Keys.DISK_DETAIL]:

        for smart in device[Keys.SMART]:
            discovery = {
                AttrKey.DISK_KEY: device[Keys.KEY],
                AttrKey.DISK_NAME: device[Keys.NAME],
                AttrKey.ATTR_ID: smart[Keys.SMART_ID],
                AttrKey.ATTR_NAME: smart[Keys.SMART_NAME]
            }

            discovery_result.append(discovery)

    data = {"request": "sender data", "data": []}
    valueStr = json.dumps({"data": discovery_result})
    send_data = {
        "host": cfg.ZABBIX_HOST,
        "key": AttrKey.ZBX_KEY,
        "value": f"{valueStr}"
    }
    data["data"].append(send_data)

    send_to_zabbix(data)

    return None


def send_smart_data(data):
    logger.info("Send S.M.A.R.T data to zabbix")

    results = []
    for device in data[Keys.DISK_DETAIL]:
        types = []
        if (cfg.SEND_SMART_VALUE): types.append(Keys.SMART_VALUE)
        if (cfg.SEND_SMART_WORST): types.append(Keys.SMART_WORST)
        if (cfg.SEND_SMART_THRESHOULD): types.append(Keys.SMART_THRESH)

        for smart in device[Keys.SMART]:

            for type in types:

                if (smart[type] == None): continue

                key = AttrKey.zabbix_key(smart[Keys.SMART_ID], type, device[Keys.KEY])

                results.append({
                    "host": cfg.ZABBIX_HOST,
                    "key": key,
                    "value": smart[type]
                })


    sender_data = {"request": "sender data", "data": results}
    send_to_zabbix(sender_data)

    return None
