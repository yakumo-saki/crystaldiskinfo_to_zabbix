from modules.const import Unit

"""SSDの書き込み許容量(TBW)を適当に決める
"""
def tbw_estimate(smartctl):
    if (smartctl["model_name"].startswith("SanDisk SDSSDH3 500G")):
        return 200 * Unit.TiB  # same as WD BLUE 3D

    return None
