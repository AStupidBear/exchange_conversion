import re


def convert_exchange(exchange, type="exchange"):
    if exchange in ["SSE", "SZSE", "BSE", "CFFEX", "DCE", "CZCE", "SHFE", "INE"]:
        i = ["SSE", "SZSE", "BSE", "CFFEX", "DCE", "CZCE", "SHFE", "INE"].index(exchange)
    elif exchange in ["XSHG", "XSHE", "XBEI", "CCFX", "XDCE", "XZCE", "XSGE", "XINE", "XSIE"]:
        i = ["XSHG", "XSHE", "XBEI", "CCFX", "XDCE", "XZCE", "XSGE", "XINE", "XSIE"].index(exchange)
    elif exchange in ["0", "1", "2", "F", "D", "Z", "S", "I"]:
        i = ["0", "1", "2", "F", "D", "Z", "S", "I"].index(exchange)
    if type == "exchange":
        return ["SSE", "SZSE", "BSE", "CFFEX", "DCE", "CZCE", "SHFE", "INE", "INE"][i]
    elif type == "jqdata":
        return ["XSHG", "XSHE", "XBEI", "CCFX", "XDCE", "XZCE", "XSGE", "XINE", "XINE"][i]
    elif type == "rootnet":
        return ["0", "1", "2", "F", "D", "Z", "S", "I", "I"][i]
    return exchange


def convert_symbol(symbol, exchange, type="exchange", year=None):
    exchange = convert_exchange(exchange, "jqdata")
    isoption = len(symbol) > 7
    if type == "exchange":
        if exchange in ["XDCE", "XSGE", "XINE"]:
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


def to_tqcode(jqcode):
    symbol, exchange = jqcode.split(".")
    exchange = convert_exchange(exchange, "exchange")
    symbol = convert_symbol(symbol, exchange, "exchange")
    return exchange + "." + symbol


def to_jqcode(tqcode, year=None):
    exchange, symbol = tqcode.split(".")
    exchange = convert_exchange(exchange, "jqdata")
    symbol = convert_symbol(symbol, exchange, "jqdata", year)
    return symbol + "." + exchange

