"""Default response codes."""


class RET:
    OK = 0
    PARAMERR = 4001
    DBERR = 4002
    NODATA = 4003
    URLNOTFOUND = 4004


error_map_EN = {
    RET.OK: "OK",
    RET.PARAMERR: "Parameter error",
    RET.DBERR: "Database error",
    RET.NODATA: "No data",
    RET.URLNOTFOUND: "URL not found",
}
