import logging
from interpriters.BaseInterpriter import BaseInterpriter
from lib.zabbix_data import get_empty_data

logger = logging.getLogger(__name__)

class SanDiskInterpriter(BaseInterpriter):
    # def __init__(self):
    #     pass

    def isTargetStrict(self, data):
        return False

    def isTargetLoose(self, data):
        return (data["model_name"].startswith("SanDisk"))

    def parse(self, data):
        logger.debug("Sandisk")
        ret = get_empty_data()
        return ret
