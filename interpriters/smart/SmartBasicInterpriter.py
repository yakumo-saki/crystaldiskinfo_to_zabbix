import logging
from interpriters.smart.SmartBaseInterpriter import SmartBaseInterpriter
from modules.const import Keys

logger = logging.getLogger(__name__)

class SmartBasicInterpriter(SmartBaseInterpriter):
    """
    最低限の解釈だけを行うInterpriter
    """

    """
    解釈を行います。
    """
    def parse(self, data):
        ret = self.basic_parse(data)
        candicate = self.get_smart(data, 233)
        if (self.isMediaWearoutIndicator(candicate)):
            ret[Keys.SSD_LIFESPAN] = candicate["value"]

        candicate = self.get_smart(data, 230)
        if (self.isMediaWearoutIndicator(candicate)):
            ret[Keys.SSD_LIFESPAN] = 100 - candicate["value"]

        return ret

    def isMediaWearoutIndicator(self, attr):
        if attr == None: return False
        if (attr["name"] == "Media_Wearout_Indicator"):
            return True
        
        return False

