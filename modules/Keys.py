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
    SSD_BYTES_WRITTEN = "ssd.bytes_written"
    SSD_LIFESPAN = "ssd.lifespan"

    @classmethod
    def zabbix_key(cls, key, dev = None):
        if (dev != None):
            return f"smartmontools.{key}[{dev}]"

        return f"smartmontools.{key}"