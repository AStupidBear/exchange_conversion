import re


def convert_exchange(exchange, type="exchange"):
    if exchange in ["SSE", "SZSE", "BSE", "CFFEX", "DCE", "CZCE", "SHFE", "INE", "GFEX"]:
        i = ["SSE", "SZSE", "BSE", "CFFEX", "DCE", "CZCE", "SHFE", "INE", "GFEX"].index(exchange)
    elif exchange in ["XSHG", "XSHE", "BJSE", "CCFX", "XDCE", "XZCE", "XSGE", "XINE", "GFEX", "XSIE", "XGFE"]:
        i = ["XSHG", "XSHE", "BJSE", "CCFX", "XDCE", "XZCE", "XSGE", "XINE", "GFEX", "XSIE", "XGFE"].index(exchange)
    elif exchange in ["0", "1", "2", "F", "D", "Z", "S", "I"]:
        i = ["0", "1", "2", "F", "D", "Z", "S", "I"].index(exchange)
    else:
        i = -1
    if type == "exchange":
        return ["SSE", "SZSE", "BSE", "CFFEX", "DCE", "CZCE", "SHFE", "INE", "GFEX", "INE", "GFEX", exchange][i]
    elif type == "jqdata":
        return ["XSHG", "XSHE", "BJSE", "CCFX", "XDCE", "XZCE", "XSGE", "XINE", "GFEX", "XINE", "GFEX", exchange][i]
    elif type == "rootnet":
        return ["0", "1", "2", "F", "D", "Z", "S", "I", "I", exchange][i]
    return exchange


def convert_symbol(symbol, exchange, type="exchange", year=None):
    exchange = convert_exchange(exchange, "jqdata")
    isoption = len(symbol) > 7
    if type == "exchange":
        if exchange in ["XDCE", "XSGE", "XINE", "GFEX"]:
            symbol = symbol.lower()
        elif exchange in ["XZCE", "CCFX"]:
            symbol = symbol.upper()
        if exchange == "XZCE"  and not isoption and re.match("[A-Z]{1,3}\d{4}", symbol):
            symbol = symbol[:-4] + symbol[-3:]
        return symbol
    elif type == "jqdata":
        symbol = symbol.upper()
        if exchange == "XZCE" and not isoption:
            if year is None:
                y = '2' if symbol[-3] in ('0', '1', '2', '3', '4') else '1'
            else:
                y = str(year)[-2]
            symbol = symbol[:-3] + y + symbol[-3:]
        return symbol


def to_tqcode(code, source="jqcode"):
    if source == "jqcode":
        symbol, exchange = code.split(".")
        exchange = convert_exchange(exchange, "exchange")
        symbol = convert_symbol(symbol, exchange, "exchange")
        return exchange + "." + symbol
    elif source == "vt_symbol":
        exchange, symbol = code.split(".")
        return exchange + "." + symbol


def to_jqcode(code, year=None, source="tqcode"):
    if source == "tqcode":
        exchange, symbol = code.split(".")
    elif source == "vt_symbol":
        exchange, symbol = code.split(".")
    else:
        raise ValueError("Invalid source: {}".format(source))
    exchange = convert_exchange(exchange, "jqdata")
    symbol = convert_symbol(symbol, exchange, "jqdata", year)
    return symbol + "." + exchange


def to_vt_symbol(code, source="jqcode"):
    if source == "jqcode":
        exchange = convert_exchange(exchange, "exchange")
        symbol = convert_symbol(symbol, exchange, "exchange")
        return symbol + "." + exchange
    elif source == "tqcode":
        exchange, symbol = code.split(".")
        return symbol + "." + exchange
    else:
        raise ValueError("Invalid source: {}".format(source))
