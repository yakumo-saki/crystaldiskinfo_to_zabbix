import logging
from modules.zabbix_data import get_empty_data
from modules.Keys import Keys

logger = logging.getLogger(__name__)

class BaseInterpriter(object):
    """
    Base class of interpriters.
    """

    def __init__(self):
        pass

    """
    指定されたモデルが解釈可能か否かを返します。
    すべてのInterpriterに対して本メソッドを呼び、最初に見つかったInterpriterに
    解釈を依頼します。
    """
    def isTargetStrict(self, data):
        return False


    """
    指定されたモデルが解釈可能かもしれないか否かを返します。
    すべてのInterpriterがisTargetStrict = False を返した場合、
    本メソッドを呼び、最初に見つかったInterpriterに解釈を依頼します。
    """
    def isTargetLoose(self, data):
        return False


    """SMARTの値を取得します。
    :param string smartctl: smartctl result
    :param int id_dec: SMART ID (decimal)
    :return: SMART Value dictionary or None
    { "id": 5, "name": "Reallocated_Sector_Ct", "value": 100, "worst": 100,
        "flags": { "value": 50, (snip)}, "raw": {"value": 0, "string": "0"}
    """
    def get_smart(self, smartctl, id_dec):
        smart_attrs = smartctl["ata_smart_attributes"]["table"]

        for attr in smart_attrs:
            if (attr["id"] != id_dec):
                continue

            return attr

        return None


    def get_smart_raw_value(self, smartctl, id_dec):

        attr = self.get_smart(smartctl, id_dec)

        if (attr == None): return None

        return attr["raw"]["value"]



    """基本的な解釈を行います。
    HDD/SSDモデルを問わず基本的に存在する最低限の部分のみを解釈します。
    """
    def basic_parse(self, smartctl):
        ret = get_empty_data()
        ret[Keys.DISK_MODEL] = smartctl["model_name"]
        ret[Keys.DISK_TYPE] = smartctl["device"]["type"] # sat scs? nvm?
        ret[Keys.DISK_PROTOCOL] = smartctl["device"]["protocol"] # ATA SAS? NVM?
        ret[Keys.DISK_ROTATION_RATE] = smartctl["rotation_rate"] # SSD = 0, HDD = 5400 7200 10000 15000
        ret[Keys.SERIAL_NUMBER] = smartctl["serial_number"]
        ret[Keys.SMART_STATUS_PASSED] = 1 if smartctl["smart_status"]["passed"] else 0
        ret[Keys.POWER_CYCLE] = smartctl["power_cycle_count"]
        ret[Keys.POWER_ON_HOURS] = smartctl["power_on_time"]["hours"]
        ret[Keys.TEMPERATURE] = smartctl["temperature"]["current"]
        
        return ret


    """
    解釈を行います。
    """
    def parse(self, data):
        logger.error("BaseInterpriter can not do `parse`")
        raise "Must override"

