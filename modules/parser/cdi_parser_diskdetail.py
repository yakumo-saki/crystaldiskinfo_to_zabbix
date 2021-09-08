import logging

from modules.const import Keys, Unit

logger = logging.getLogger(__name__)


"""ディスク詳細のヘッダの名前を1行解釈する
cf) "(01) WDC WD30EFRX-68EUZN0"
"""
def parse_diskdetail_header(detail, line):
    ln = line.strip()

    detail[Keys.ID] = ln[0:4]    # "(01)"
    detail[Keys.MODEL] = ln[5:].strip()   # "WDC WD30EFRX-68AX9N0"

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
    CDI_KEY_TO_MY_KEY = {
        "Firmware": Keys.FIRMWARE,
        "Serial Number": Keys.SERIAL_NUMBER,
        "Disk Size": Keys.DISK_SIZE,
        "Interface": Keys.INTERFACE,
        "Power On Hours": Keys.POWER_ON_HOURS,
        "Power On Count": Keys.POWER_ON_COUNT,
        "Temperature": Keys.TEMPERATURE,
        "Health Status": Keys.HEALTH_STATUS,
        "Host Reads": Keys.HOST_READS,
        "Host Writes": Keys.HOST_WRITES,
        "NAND Writes": Keys.NAND_WRITES,
        "Wear Level Count": Keys.WEAR_LEVEL_COUNT,
    }

    # 存在することは知っているが送信しないキー
    IGNORE = [
        "Buffer Size", "Queue Depth", "# of Sectors",
        "Rotation Rate", "Major Version", "Minor Version",
        "Transfer Mode", "Features", "APM Level", "AAM Level",
        "Drive Letter", "Model"
        ]

    convmaps = {
        Keys.DISK_SIZE: _WithUnitToByte,
        Keys.NAND_WRITES: _WithUnitToByte,
        Keys.HOST_READS: _WithUnitToByte,
        Keys.HOST_WRITES: _WithUnitToByte,
        Keys.POWER_ON_HOURS: _deleteUnit,
        Keys.POWER_ON_COUNT: _deleteUnit,
        Keys.TEMPERATURE: _deleteUnit
    }

    if key not in CDI_KEY_TO_MY_KEY:
        if key not in IGNORE:
            logger.warn(f"Unknown key {key}. Please notify author.")
        return None

    itemKey = CDI_KEY_TO_MY_KEY[key]
    if (itemKey == Keys.HEALTH_STATUS):
        (status, life) = _parseHealth(value)
        detail[Keys.HEALTH_STATUS] = status
        detail[Keys.LIFESPAN] = life
    elif (itemKey in convmaps):
        # 変換用メソッドがあるので呼ぶ
        detail[itemKey] = convmaps[itemKey](value)
    else:
        detail[itemKey] = value

    return None


"""GB等をbyte単位にする
注意： nnn.n GB のあとは無視される
パターン1 "250.0 GB (8.4/137.4/250.0/250.0)" <- SATA
パターン2 "512.1 GB" <- NVMe
"""
def _WithUnitToByte(value):
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