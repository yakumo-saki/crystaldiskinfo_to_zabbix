import logging

from modules.const import Unit
from modules.parser.cdi_const import RS_DISKLIST, RS_DISK_SMART

import copy

logger = logging.getLogger(__name__)


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
    keymaps = {
        "Firmware": "firmware",
        "Serial Number": "serialNumber",
        "Disk Size": "diskSize",
        "Interface": "interface",
        "Power On Hours": "powerOnHours",
        "Power On Count": "powerOnCount",
        "Temperature": "temperature",
        "Health Status": "healthStatus"
    }

    convmaps = {
        "Disk Size": _diskSize
    }

    for k, v in keymaps.items():
        if (key == k):
            if (key in convmaps):
                # 変換用メソッドがある
                detail[v] = convmaps[key](value)
            else:
                detail[v] = value
            
            break

    return None


"""
パターン1 "250.0 GB (8.4/137.4/250.0/250.0)", SATA
パターン2 "512.1 GB", NVMe
"""
def _diskSize(value):
    v = value.split(" ", maxsplit=2)

    num = float(v[0])
    unit = v[1].strip()

    if (unit == "GB"):
        return int(num * Unit.GiB)
    elif (unit == "MB"):
        return int(num * Unit.MiB)
    elif (unit == "TB"):
        return int(num * Unit.TiB)

    return num