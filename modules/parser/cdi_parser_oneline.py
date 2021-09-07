import logging
from modules.const import Keys
from modules.parser.cdi_const import RS_DISKLIST, RS_DISK_SMART

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


"""ディスク詳細のヘッダの名前を1行解釈する
cf) "(01) WDC WD30EFRX-68EUZN0"
"""
def parse_diskdetail_header(detail, line):
    ln = line.strip()

    detail["id"] = ln[0:4]    # "(01)"
    detail["model"] = ln[5:].strip()   # "WDC WD30EFRX-68AX9N0"

    return None


"""ディスク詳細を1行解釈してdetailに追加する
cf) "           Model : WDC WD30EFRX-68AX9N0"
"""
def parse_diskdetail_body(detail, line):
    ln = line.strip()

    attr = ln.split(":", maxsplit=1)
    key = attr[0].strip()
    value = attr[1].strip()

    # CDI出力 -> key
    maps = {
        "Firmware": "firmware",
        "Serial Number": "serialNumber",
        "Disk Size": "diskSize",
        "Interface": "interface",
        "Power On Hours": "powerOnHours",
        "Power On Count": "powerOnCount",
        "Temperature": "temperature",
        "Health Status": "healthStatus"
    }

    for k, v in maps.items():
        if (key == k):
            detail[v] = value

    return None


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
    logger.debug(smartAttr)
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