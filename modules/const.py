from dataclasses import dataclass
class Unit():
    KB = 1024
    MB = 1024 * 1024
    GB = 1024 * 1024 * 1024
    TB = 1024 * 1024 * 1024 * 1024
    SI = 1000
    KiB = 1000
    MiB = 1000 * 1000
    GiB = 1000 * 1000 * 1000
    TiB = 1000 * 1000 * 1000 * 1000

class Keys():

    ID = "id"
    KEY = "key"   # zabbix上のディスクに対する一意なキー 
    NAME = "name" # zabbix上の表示名
    MODEL = "model"
    FIRMWARE = "firmware"
    SERIAL_NUMBER = "serialNumber"
    INTERFACE = "interface"
    DISK_SIZE = "diskSize"
    POWER_ON_HOURS = "powerOnHours"
    POWER_ON_COUNT = "powerOnCount"
    TEMPERATURE = "temperature"
    HEALTH_STATUS = "healthStatus"
    HOST_WRITES = "hostWrites"
    HOST_READS = "hostReads"
    NAND_WRITES = "nandWrites"
    WEAR_LEVEL_COUNT = "wearLevelCount"
    LIFESPAN = "lifespan"
    SMART = "smart"

    SMART_ID = "id"
    SMART_NAME = "name"
    SMART_VALUE = "value"
    SMART_WORST = "worst"
    SMART_THRESH = "threshould"


    @classmethod
    def zabbix_key(cls, key, dev = None):
        if (dev != None):
            return f"crystaldisk.{key}[{dev}]"

        return f"crystaldisk.{key}"


@dataclass
class DeviceKey():
    """Zabbixのデバイスディスカバリに使うキー
    """


    ZBX_KEY = 'crystaldisk.discovery.device'
    DISK_KEY = '{#KEY}'
    """ アイテムキーに使うキー (シリアルNO)"""
    DISK_NAME = '{#NAME}'
    """ 表示名 """


class AttrKey():
    """ZabbixのSMART属性ディスカバリに使うキー
    """
    ZBX_KEY = 'crystaldisk.discovery.smart'
    DISK_KEY = '{#KEY}'    # アイテムキーに使うキー (シリアルNO)
    DISK_NAME = "{#NAME}"
    ATTR_NAME = "{#ATTRNAME}"
    ATTR_ID = "{#ATTRID}"

    # {0} = device  {1} = attr id
    THRESH_KEY = "crystaldisk.smart.threshould[{0},{1}]"
    VALUE_KEY = "crystaldisk.smart.value[{0},{1}]"
    WORST_KEY = "crystaldisk.smart.worst[{0},{1}]"
