from enum import Enum

class Keys(Enum):
    POWER_CYCLE = "power_cycle"
    ROTATION_RATE = "rotation_rate"
    POWER_ON_HOURS = "power_on_hours"
    TEMPERATURE = "temperature"
    DISK_MODEL = "model"
    DISK_TYPE = "type"
    DISK_ROTATION_RATE = "rotation_rate"
    SSD_BYTES_WRITTEN = "ssd-bytes_written"
    SSD_LIFESPAN = "ssd-lifespan"

    @classmethod
    def zabbix_key(cls, key):
        key.replace("-", ".")