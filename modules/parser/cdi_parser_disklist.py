import logging
from modules.const import Keys
from modules.parser.cdi_const import RS_DISKLIST

import copy

logger = logging.getLogger(__name__)


"""ディスク一覧を1行解釈する
cf) "(01) WDC WD30EFRX-68EUZN0 : 3000.5 GB [X/0/0, mr]"
"""
def parse_disklist(line):
    ln = line.strip()
    result = copy.deepcopy(RS_DISKLIST)

    result["id"] = ln[0:4]    # "(01)"
    result["model"] = ln[5:ln.index(":")].strip()   # "WDC WD30EFRX-68AX9N0"
    
    # commandType
    ct = ln[ln.index("[") + 1:ln.index("]")].strip()  # X/0/0, mr
    result["commandType"] = ct[ct.index(",") + 1:].strip()

    # ssdVendorString
    svs = ln[ln.index("]"):]

    if (svs.find("-") > 0):    # SSD以外の場合この部分は出てこない
        result["ssdVendorString"] = svs[svs.index("-") + 1:].strip()
    
    return result


