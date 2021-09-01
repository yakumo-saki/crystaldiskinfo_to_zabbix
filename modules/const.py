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
    DISK_MODEL = "model"
    DISK_TYPE = "type"
    DISK_PROTOCOL = "protocol"
    DISK_ROTATION_RATE = "rotation_rate"
    SERIAL_NUMBER = "serial_number"
    SMART_STATUS_PASSED = "smart_status_passed"

    POWER_CYCLE = "power_cycle"
    POWER_ON_HOURS = "power_on_hours"
    TEMPERATURE = "temperature"
    SSD_BYTES_WRITTEN_MAX = "ssd.bytes_written_max"  # = TBW
    SSD_BYTES_WRITTEN = "ssd.bytes_written"
    SSD_LIFESPAN = "ssd.lifespan"

    @classmethod
    def zabbix_key(cls, key, dev = None):
        if (dev != None):
            return f"smartmontools.{key}[{dev}]"

        return f"smartmontools.{key}"