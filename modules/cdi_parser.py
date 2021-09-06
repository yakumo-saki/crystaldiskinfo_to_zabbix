from modules.const import Keys

class Pos():
    """ヘッダ部の文字列兼、フラグ文字列
    """
    DISKLIST = "-- Disk List"


RS_DISKLIST = {
    "id": None,    # "01" "02"
    "model": None, # "WDC WD30EFRX-68AX9N0"
    "bus": None,   # AtaSmart.h commandTypeString
}


class Result():
    disklist = {}   # key = ID "01" "02" ... 
    disk_detail = {}   # 

def parse(path):
    print(path)
    with open(path) as f:
        for line in f:
            if (line.strip() == ""):
                continue  # 空行はスルー

            print(line.rstrip())

            if (Pos.DISKLIST in line):
                pass
