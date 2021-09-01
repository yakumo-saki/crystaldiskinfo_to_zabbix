import logging
from interpriters.BaseInterpriter import BaseInterpriter
from modules.const import Keys

logger = logging.getLogger(__name__)

class BasicInterpriter(BaseInterpriter):
    """
    最低限の解釈だけを行うInterpriter
    """

    """
    解釈を行います。
    """
    def parse(self, data):
        ret = self.basic_parse(data)

        ret[Keys.SSD_BYTES_WRITTEN] = self.get_smart_raw_value(data, 233)

        return ret

