import logging
from interpriters.BaseInterpriter import BaseInterpriter

logger = logging.getLogger(__name__)

class SanDiskInterpriter(BaseInterpriter):
    # def __init__(self):
    #     pass

    def isTargetStrict(self, data):
        return (data["model_name"].startswith("SanDisk"))

    def isTargetLoose(self, data):
        return (data["model_name"].startswith("SanDisk"))

    def parse(self, data):
        logger.debug("Sandisk")
        return data
