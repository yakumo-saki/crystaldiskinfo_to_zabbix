import logging
from modules.const import Keys
from modules.parser.cdi_const import RS_DISK_SMART

import copy

logger = logging.getLogger(__name__)


def isNvme(detail):
    return "NVM Express" in detail["interface"]


"""ディスク詳細のSMART部を1行解釈してdetail.smartに追加する
cf) "01 200 200 _51 000000000000 リードエラーレート"
"""
def parse_diskdetail_smart(detail, line):
    import copy
    smart = copy.deepcopy(RS_DISK_SMART)

    # NVMe or else
    if isNvme(detail):
        parse_diskdetail_smart_nvme(smart, line)
    else:
        parse_diskdetail_smart_non_nvme(smart, line)

    detail["smart"].append(smart)

    return None

"""SMARTの値の桁揃えを解除
cf) _15 -> 15 __0 -> 0
"""
def parse_smart_value(numString):
    return numString.replace("_", "").strip()


"""ディスク詳細のSMART部を1行解釈してdetail.smartに追加する
cf) "01 200 200 _51 000000000000 リードエラーレート"
"""
def parse_diskdetail_smart_non_nvme(smart, line):

    ln = line.strip()

    smartAttr = ln.split(" ", maxsplit=5)  # Attribute Name部はスペースが入りうるので個数指定
    smart["id"] = smartAttr[0].strip()
    smart["name"] = smartAttr[5].strip()
    smart["value"] = parse_smart_value(smartAttr[1])
    smart["worst"] = parse_smart_value(smartAttr[2])
    smart["threshould"] = parse_smart_value(smartAttr[3])

    return smart


def parse_diskdetail_smart_nvme(smart, line):

    ln = line.strip()

    smartAttr = ln.split(" ", maxsplit=2)  # Attribute Name部はスペースが入りうるので個数指定
    
    # TODO 調整
    smart["id"] = smartAttr[0].strip()
    smart["name"] = smartAttr[2].strip()

    # TODO RawValues -> value
    smart["value"] = parse_smart_rawvalue(smartAttr[1])

    return smart


"""RawValueが16進数なので10進数にする
"""
def parse_smart_rawvalue(rawValue):
    return int(rawValue, 16)