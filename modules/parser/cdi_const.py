from modules.const import Keys

"""ディスク一覧部分のデータ雛形"""
RS_DISKLIST = {
    Keys.ID: None,               # "(01)" "(02)" "(03)"
    Keys.MODEL: None,            # "WDC WD30EFRX-68AX9N0"
    "commandType": None,      # ここからしか取れない AtaSmart.h commandTypeString
    "ssdVendorString": None,  # ここからしか取れない AtaSmart.h ssdVendorString
}

"""ディスク詳細部分のデータ雛形"""
RS_DISK_DETAIL = {
    Keys.ID: None,               # "(01)" "(02)" "(03)"
    Keys.KEY: None,              # SerialNo or (no serialNo) id + model
    Keys.MODEL: None,
    Keys.FIRMWARE: None,
    Keys.SERIAL_NUMBER: None,
    Keys.INTERFACE: None,
    Keys.DISK_SIZE: None,
    Keys.POWER_ON_HOURS: None,
    Keys.POWER_ON_COUNT: None,
    Keys.TEMPERATURE: None,
    Keys.HEALTH_STATUS: None,
    Keys.LIFESPAN: None,
    Keys.SMART: []
}

"""SMART値部分のデータ雛形"""
RS_DISK_SMART = {
    Keys.SMART_ID: None,
    Keys.SMART_NAME: None,
    Keys.SMART_VALUE: None,
    Keys.SMART_WORST: None,
    Keys.SMART_THRESH: None
} 


""" commandTypeString をわかりやすい文字列にする
AtaSmart.h
"""
def commandTypeStringToString(commandTypeString):

    if (commandTypeString.startswith("ns")):
        return "NVMe Samsung" + commandTypeString[3:]
    elif (commandTypeString.startswith("ni")):
        return "NVMe Intel" + commandTypeString[3:]
    elif (commandTypeString.startswith("sq")):
        return "NVMe Storage Query" + commandTypeString[3:]
    elif (commandTypeString.startswith("nj")):
        return "NVMe JMicron" + commandTypeString[3:]
    elif (commandTypeString.startswith("na")):
        return "NVMe ASMedia" + commandTypeString[3:]
    elif (commandTypeString.startswith("nr")):
        return "NVMe Realtek" + commandTypeString[3:]
    elif (commandTypeString.startswith("nt")):
        return "NVMe Intel RST" + commandTypeString[3:]
    elif (commandTypeString.startswith("mr")):
        return "MegaRAID SAS" + commandTypeString[3:]
    else:
        return commandTypeString


""" ssdVendorString をわかりやすい文字列にする
AtaSmart.h
"""
def ssdVendorStringToString(ssdVendorString):
    
    if (ssdVendorString.startswith("mt")):
        return "MTron" + ssdVendorString[3:]
    elif (ssdVendorString.startswith("ix")):
        return "Indilinx" + ssdVendorString[3:]
    elif (ssdVendorString.startswith("jm")):
        return "JMicron" + ssdVendorString[3:]
    elif (ssdVendorString.startswith("il")):
        return "Intel" + ssdVendorString[3:]
    elif (ssdVendorString.startswith("sg")):
        return "SAMSUNG" + ssdVendorString[3:]
    elif (ssdVendorString.startswith("sf")):
        return "SandForce" + ssdVendorString[3:]
    elif (ssdVendorString.startswith("mi")):
        return "Micron" + ssdVendorString[3:]
    elif (ssdVendorString.startswith("oz")):
        return "OCZ" + ssdVendorString[3:]
    elif (ssdVendorString.startswith("st")):
        return "SEAGATE" + ssdVendorString[3:]
    elif (ssdVendorString.startswith("wd")):
        return "WDC" + ssdVendorString[3:]
    elif (ssdVendorString.startswith("px")):
        return "PLEXTOR" + ssdVendorString[3:]
    elif (ssdVendorString.startswith("sd")):
        return "SanDisk" + ssdVendorString[3:]
    elif (ssdVendorString.startswith("oz")):
        return "OCZ Vector" + ssdVendorString[3:]
    elif (ssdVendorString.startswith("to")):
        return "TOSHIBA" + ssdVendorString[3:]
    elif (ssdVendorString.startswith("co")):
        return "Corsair" + ssdVendorString[3:]
    elif (ssdVendorString.startswith("ki")):
        return "Kingston" + ssdVendorString[3:]
    elif (ssdVendorString.startswith("m2")):
        return "Micron MU02" + ssdVendorString[3:]
    elif (ssdVendorString.startswith("nv")):
        return "NVMe" + ssdVendorString[3:]
    elif (ssdVendorString.startswith("re")):
        return "Realtek" + ssdVendorString[3:]
    elif (ssdVendorString.startswith("sk")):
        return "SKhynix" + ssdVendorString[3:]
    elif (ssdVendorString.startswith("ki")):
        return "KIOXIA" + ssdVendorString[3:]
    elif (ssdVendorString.startswith("ss")):
        return "SSSTC" + ssdVendorString[3:]
    elif (ssdVendorString.startswith("id")):
        return "Intel DC" + ssdVendorString[3:]
    elif (ssdVendorString.startswith("ap")):
        return "Apacer" + ssdVendorString[3:]
    elif (ssdVendorString.startswith("sm")):
        return "SiliconMotion" + ssdVendorString[3:]
    elif (ssdVendorString.startswith("ph")):
        return "Phison" + ssdVendorString[3:]
    elif (ssdVendorString.startswith("ma")):
        return "Marvell" + ssdVendorString[3:]
    elif (ssdVendorString.startswith("mk")):
        return "Maxiotek" + ssdVendorString[3:]
    elif (ssdVendorString.startswith("ym")):
        return "YMTC" + ssdVendorString[3:]
    else:
        return ssdVendorString