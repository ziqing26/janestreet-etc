BUFFER_SIZE = 2
CONVERSION_COST = 100
UNIT_SIZE = 10

def get_xlf_value(bond, gs, ms, wfc, dir):
    return 3 * 1000 + 2 * gs[dir][0][0] + 3 * ms[dir][0][0] + 2 * wfc[dir][0][0]

def __transact_xlf_constituents(bond, gs, ms, wfc, direction):
    opp_dir = "BUY" if direction == "SELL" else "SELL"
    transact = [
        # {"type": "ADD", "symbol": "BOND", "dir": direction,
        #     "price": bond[opp_dir][0][0], "size": 3},
        {"type": "ADD", "symbol": "GS", "dir": direction,
            "price": gs[opp_dir][0][0], "size": 2},
        {"type": "ADD", "symbol": "MS", "dir": direction,
            "price": ms[opp_dir][0][0], "size": 3},
        {"type": "ADD", "symbol": "WFC", "dir": direction,
            "price": wfc[opp_dir][0][0], "size": 2},
    ]
    return transact

def sell_at_xlf(bond, gs, ms, wfc, xlf):
    buy_xlf_constituents = __transact_xlf_constituents(bond, gs, ms, wfc, "BUY")
    convert = [{"type": "CONVERT", "symbol": "XLF", "dir": "BUY", "size": 10}]
    sell_xlf = [{"type": "ADD", "symbol": "XLF", "dir": "SELL",
                "price": xlf["BUY"][0][0], "size": 10}]
    return buy_xlf_constituents + convert + sell_xlf

def buy_at_xlf(bond, gs, ms, wfc, xlf):
    sell_xlf_constituents = __transact_xlf_constituents(bond, gs, ms, wfc, "SELL")
    return [
            {"type": "ADD", "symbol": "XLF", "dir": "BUY",
                "price": xlf["SELL"][0][0], "size": 10},
            {"type": "CONVERT", "symbol": "XLF", "dir": "SELL", "size": 10},
        ] + sell_xlf_constituents

def xlf_action(bond, gs, ms, wfc, xlf):
    if not (gs and ms and wfc and xlf):
        return []
    if not (gs["BUY"] and ms["BUY"] and wfc["BUY"] and xlf["BUY"]):
        return []
    if not (gs["SELL"] and ms["SELL"] and wfc["SELL"] and xlf["SELL"]):
        return []

    if get_xlf_value(bond, gs, ms, wfc, "SELL") + CONVERSION_COST + BUFFER_SIZE < (xlf["BUY"][0][0] * UNIT_SIZE):
        return sell_at_xlf(bond, gs, ms, wfc, xlf)
    elif get_xlf_value(bond, gs, ms, wfc, "BUY") > (xlf["SELL"][0][0] * UNIT_SIZE + CONVERSION_COST + BUFFER_SIZE):
        return buy_at_xlf(bond, gs, ms, wfc, xlf)
