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
        "Disk Size": _diskSize,
        "Power On Hours": _deleteUnit,
        "Power On Count": _deleteUnit,
        "Temperature": _deleteUnit
    }

    for k, v in keymaps.items():
        if (key == k):
            if (key == "Health Status"):
                (status, life) = _parseHealth(value)
                detail["healthStatus"] = status
                detail["lifespan"] = life
            elif (key in convmaps):
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


"""単位部分以降を削除する。
250 時間 -> 250  / 123 回 -> 123
"""
def _deleteUnit(value):
    return int(value[0:value.index(" ")])


"""Health Statusを解釈する
return "正常" -> 正常,None （そのまま）
return "正常 (30 %) -> 正常,30 （SSD。寿命を別で返す）
"""
def _parseHealth(value):
    # 寿命が含まれなければそのまま返して抜ける
    if (value.find("(") < 0):
        return value, None

    # 寿命を抜き出す
    lifeStr = value[value.index("(") + 1:value.index(" %")]
    life = int(lifeStr)
    stat = value[0:value.index(" ")]
    return stat, life