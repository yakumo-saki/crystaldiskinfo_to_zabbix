import logging
from modules.zabbix_data import get_empty_data
from const import Keys

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


    """基本的な解釈を行います。
    HDD/SSDモデルを問わず基本的に存在する最低限の部分のみを解釈します。
    """
    def basic_parse(self, data):
        ret = get_empty_data()
        ret[Keys.DISK_MODEL] = data["model_name"]
        ret[Keys.DISK_TYPE] = data["device"]["type"] # sat scs? nvm?
        ret[Keys.DISK_PROTOCOL] = data["device"]["protocol"] # ATA SAS? NVM?
        ret[Keys.DISK_ROTATION_RATE] = data["rotation_rate"] # SSD = 0, HDD = 5400 7200 10000 15000
        ret[Keys.SERIAL_NUMBER] = data["serial_number"]
        ret[Keys.SMART_STATUS_PASSED] = 1 if data["smart_status"]["passed"] else 0
        
        return ret


    """
    解釈を行います。
    """
    def parse(self, data):
        logger.error("BaseInterpriter can not do `parse`")
        raise "Must override"

