import logging

from interpriters.smart.SmartBaseInterpriter import SmartBaseInterpriter
from modules.const import Keys, Unit
from interpriters.tbw_estimate import tbw_estimate

logger = logging.getLogger(__name__)

"""
SanDisk SSDSSDH3 -> Marvel 88SS1074
"""
class SmartSanDiskInterpriter(SmartBaseInterpriter):
    # def __init__(self):
    #     pass

    def isTargetStrict(self, data):
        if (data["model_name"].startswith("SanDisk SDSSDH3")):
            return True

        return False

    def isTargetLoose(self, data):
        return (data["model_name"].startswith("SanDisk"))

    def parse(self, data):
        logger.debug("Sandisk")
        ret = self.basic_parse(data)

        # 233 Media Wearout Indicator
        ret[Keys.SSD_LIFESPAN] = self.get_smart_value(data, 233)

        # 241 Total_LBAs_Written は名前に反してそのままGB単位
        ret[Keys.SSD_BYTES_WRITTEN] = (self.get_smart_raw_value(data, 241) * Unit.GB)
        ret[Keys.SSD_BYTES_WRITTEN_MAX] = tbw_estimate(data)

        return ret
