import logging
from interpriters.BaseInterpriter import BaseInterpriter

from lib.zabbix_data import get_empty_data

logger = logging.getLogger(__name__)

class BasicInterpriter(BaseInterpriter):
    """
    最低限の解釈だけを行うInterpriter
    """

    """
    解釈を行います。
    """
    def parse(self, data):
        ret = get_empty_data()
        return ret

