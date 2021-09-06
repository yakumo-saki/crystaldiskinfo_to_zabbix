import logging
from modules.const import Keys

logger = logging.getLogger(__name__)

class Keyword():
    """ヘッダ部の文字列兼、フラグ文字列
    """
    DISK_LIST = "-- Disk List"
    DISK_DETAIL = "---------------"
    DISK_SMART = "-- S.M.A.R.T."


class Pos():
    DISK_LIST = "DISK_LIST"
    DISK_DETAIL_HEAD = "DISK_DETAIL_HEAD"   # (01) WDC WD30〜　のような名称
    DISK_DETAIL_BODY = "DISK_DETAIL_BODY"
    DISK_SMART_HEAD = "DISK_SMART_HEAD"    # SMARTヘッダ "ID Cur Wor Thr ..."
    DISK_SMART_BODY = "DISK_SMART"      # SMART情報部
    DISK_DETAIL_END = "DISK_DETAIL_END"  # 次のディスク情報まで読み飛ばし


class Result():
    disklist = []      # key = ID "(01)" "(02)" ... 
    disk_detail = []   # 


# Result.disklist
RS_DISKLIST = {
    "id": None,               # "(01)" "(02)" "(03)"
    "model": None,            # "WDC WD30EFRX-68AX9N0"
    "commandType": None,      # ここからしか取れない AtaSmart.h commandTypeString
    "ssdVendorString": None,  # ここからしか取れない AtaSmart.h ssdVendorString
}

RS_DISK_DETAIL = {
    "id": None,
    "model": None,
    "firmware": None,
    "SerialNumber": None,
    "DiskSize": None,
    "PowerOnHours": None,
    "PowerOnCount": None,
    "Temperature": None,
    "HealthStatus": None,
    "Smart": []
}

RS_DISK_SMART = {
    "id": None,
    "name": None,
    "value": None,
    "worst": None,
    "threshould": None
} 


def parse(path):
    import copy

    now = None   # 現在のブロック
    result = Result()

    print(path)
    with open(path) as f:

        detail = None
        lineNo = 0
        for line in f:
            line = line.rstrip()
            lineNo += 1

            if now == None:
                if (line.startswith(Keyword.DISK_LIST)):
                    now = Pos.DISK_LIST

                continue  # Disk list が出てくるまで読み飛ばし
            elif now == Pos.DISK_LIST:
                if (line.strip() == ""):
                    pass   # 空行は読み飛ばす。空行の次にDisk詳細が来る
                elif (line.startswith(Keyword.DISK_DETAIL)):
                    now = Pos.DISK_DETAIL_HEAD
                    logger.debug("NEXT DISK_DETAIL_HEAD")
                else:
                    result.disklist.append(parse_disklist(line))

                continue
            elif now == Pos.DISK_DETAIL_HEAD:
                # --------------------------------------------
                # ↑の行
                # ここからディスク詳細DISK_DETAIL
                if (line.startswith(Keyword.DISK_DETAIL)):
                    now = Pos.DISK_DETAIL_BODY
                    logger.debug("NEXT DISK_DETAIL_BODY")
                else:
                    detail = copy.deepcopy(RS_DISK_DETAIL)
                    parse_diskdetail_header(detail, line)

                continue
            elif now == Pos.DISK_DETAIL_BODY:

                if (line.strip() == ""):
                    # expected, final empty line
                    pass
                elif (line.startswith(Keyword.DISK_SMART)):
                    now = Pos.DISK_SMART_HEAD
                    logger.debug("NEXT DISK_SMART_HEAD")
                else:
                    parse_diskdetail_body(detail, line)

                continue
            elif now == Pos.DISK_SMART_HEAD:
                # ID Cur Wor Thr の行。読まない

                if (line.strip() == ""):
                    raise "Unexpected"
                else:
                    now = Pos.DISK_SMART_BODY
                    logger.debug("NEXT DISK_SMART_BODY")

                continue
            elif now == Pos.DISK_SMART_BODY:
                if (line.strip() == ""):
                    now = Pos.DISK_DETAIL_END
                    logger.debug("NEXT DISK_DETAIL_END ---------------")
                else:
                    parse_diskdetail_smart(detail, line)    

                continue
            elif now == Pos.DISK_DETAIL_END:
                # SMART情報が終わったらあとは次まで読み飛ばし
                if (line.startswith(Keyword.DISK_DETAIL)):
                    # 次のディスクの情報に移った
                    now = Pos.DISK_DETAIL_HEAD
                    logger.debug("NEXT DISK_DETAIL_HEAD")
                else:
                    # print("ignore " + line)
                    pass

                continue


"""ディスク一覧を1行解釈する
cf) "(01) WDC WD30EFRX-68EUZN0 : 3000.5 GB [X/0/0, mr]"
"""
def parse_disklist(line):
    print("DISKLIST " + line)
    return {}


"""ディスク詳細のヘッダの名前を1行解釈する
cf) "(01) WDC WD30EFRX-68EUZN0"
"""
def parse_diskdetail_header(datail, line):
    print("DISK_DETAIL_HEAD " + line)
    return {}


"""ディスク詳細を1行解釈してdetailに追加する
cf) "           Model : WDC WD30EFRX-68AX9N0"
"""
def parse_diskdetail_body(datail, line):
    #print("DISK_DETAIL_BODY " + line)
    return None

"""ディスク詳細のSMART部を1行解釈してdetail.smartに追加する
cf) "01 200 200 _51 000000000000 リードエラーレート"
"""
def parse_diskdetail_smart(datail, line):
    #print("SMART " + line)
    return None