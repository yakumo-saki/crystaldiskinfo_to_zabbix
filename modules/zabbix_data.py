from modules.const import Keys
import copy 

# parse後のデータ
PARSED_DATA = {
    Keys.DISK_MODEL: None,
    Keys.DISK_TYPE: None,
    Keys.DISK_ROTATION_RATE: None,
    Keys.DISK_PROTOCOL: None,
    Keys.SERIAL_NUMBER: None,
    Keys.POWER_CYCLE: None,
    Keys.POWER_ON_HOURS: None,
    Keys.TEMPERATURE: None,
    Keys.SSD_BYTES_WRITTEN: None,
    Keys.SSD_LIFESPAN: None,
}


def get_empty_data():
    return copy.deepcopy(PARSED_DATA)