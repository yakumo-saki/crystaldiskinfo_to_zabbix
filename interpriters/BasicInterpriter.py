import logging
from interpriters.BaseInterpriter import BaseInterpriter

logger = logging.getLogger(__name__)

class BasicInterpriter(BaseInterpriter):
    """
    最低限の解釈だけを行うInterpriter
    """

    # def __init__(self):
    #     pass


    """
    解釈を行います。
    """
    def parse(self, data):
        logger.error("BaseInterpriter can not do `parse`")
        raise "Must override"

