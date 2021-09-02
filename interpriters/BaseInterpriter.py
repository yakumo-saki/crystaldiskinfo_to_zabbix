import logging
from modules.zabbix_data import get_empty_data
from modules.const import Keys

logger = logging.getLogger(__name__)

class BaseInterpriter(object):
    """
    Base class interpriters.
    """

    def __init__(self):
        pass

    """デバイスタイプ（SATA,SCSI,NVME)が処理対象かを返す
    """
    def isTargetDeviceType(self, data):
        raise "MustOverride"

    """
    指定されたモデルが解釈可能か否かを返します。
    すべてのInterpriterに対して本メソッドを呼び、最初に見つかったInterpriterに
    解釈を依頼します。
    """
    def isTargetStrict(self, data):
        raise "MustOverride"


    """
    指定されたモデルが解釈可能かもしれないか否かを返します。
    すべてのInterpriterがisTargetStrict = False を返した場合、
    本メソッドを呼び、最初に見つかったInterpriterに解釈を依頼します。
    """
    def isTargetLoose(self, data):
        raise "MustOverride"


    """
    解釈を行います。
    """
    def parse(self, data):
        logger.error("BaseInterpriter can not do `parse`")
        raise "Must override"

