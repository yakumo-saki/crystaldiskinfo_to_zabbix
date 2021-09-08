import logging

import config as cfg
from modules.parser.cdi_parser_disklist import parse_disklist
from modules.parser.cdi_parser_diskdetail import parse_diskdetail_header, parse_diskdetail_body
from modules.parser.cdi_parser_smart import parse_diskdetail_smart
from modules.parser.cdi_const import RS_DISK_DETAIL, RS_DISKLIST

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


RESULT = {
    "diskList": [],     # key = ID "(01)" "(02)" ... 
    "diskDetail": []   # 
}

def parse(path):
    import copy

    now = None   # 現在のブロック
    result = copy.deepcopy(RESULT)

    logger.debug(f"Opening file: {path}")
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
                    result["diskList"].append(parse_disklist(line))

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
                    result["diskDetail"].append(detail)
                    parse_diskdetail_header(detail, line)

                continue
            elif now == Pos.DISK_DETAIL_BODY:

                if (line.strip() == ""):
                    key = _createKey(detail)
                    detail["key"] = key
                    logger.debug(f"DISK_DETAIL_BODY END KEY={key}")
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

    logger.debug("parse done")

    import json
    if (cfg.PARSED_JSON != ""):
        logger.debug(f"Exporting parsed.json: {cfg.PARSED_JSON}")
        with open(cfg.PARSED_JSON, 'w', encoding='UTF-8') as f:
            f.write(json.dumps(result, indent=2, ensure_ascii=False))

    return result


def _createKey(detail):
    if (detail["serialNumber"] == "************"):
        logger.info("Serial Number is hidden. It is not recommended."
        + " Change setting on CrystalDiskInfo GUI.")
        model = detail["model"]
        model = model.replace(" ", "_")
        return detail["id"] + model

    return detail["serialNumber"]
    
