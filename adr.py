# from main import *
# def convert(from_stock, to_tock, quantity):
#     pass

# def actions(bond, quantity, price):
#     pass

import time 

def format_action(symbol, direction, price, size):
    return {"type": "ADD", "symbol": symbol, "dir": direction, "price": price, "size": size}

def convert(from_stock, to_stock, size):
    return {"type": "CONVERT", "symbol": to_stock, "dir": "BUY", "size": size}

def adr_action(trade_info, symbol_pos):
    actions = []
    awake = 1
    time = time.now()
    if abs(symbol_pos["VALE"]) == 10 and abs(symbol_pos["VALBZ"]) == 10 and awake:
        print("VALE number " + symbol_pos["VALE"], "VALBZ number " + symbol_pos["VALBZ"])
        if symbol_pos["VALE"] == 10:
            from_stock = "VALE"
            to_stock = "VALBZ"
        else:
            from_stock = "VALBZ" 
            to_stock = "VALE"
        # actions.append(convert(from_stock, to_stock, 10))
        awake = 0

    if trade_info["valbz_bid"][0] > trade_info["vale_ask"][0] + 2:
        # print("I am here")
        from_stock = "VALE"
        from_price = trade_info["vale_ask"][0]
        to_stock = "VALBZ"
        to_price = trade_info["valbz_bid"][0]
        quantity = trade_info["vale_ask"][1]

        actions.append(format_action(from_stock, "BUY", from_price, quantity))
        actions.append(convert(from_stock, to_stock, quantity))
        actions.append(format_action(to_stock, "SELL",to_price, round(quantity*0.6)))
        actions.append(format_action(to_stock, "SELL",to_price - 1, round(quantity*0.4)))


    if trade_info["vale_bid"][0] > trade_info["valbz_ask"][0] + 2:
        # print("I am here")
        from_stock = "VALBZ"
        from_price = trade_info["valbz_ask"][0]
        to_stock = "VALE"
        to_price = trade_info["valbz_bid"][0]
        quantity = trade_info["valbz_ask"][1]

        actions.append(format_action(from_stock, "BUY", from_price, quantity))
        actions.append(convert(from_stock, to_stock, quantity))
        actions.append(format_action(to_stock, "SELL",to_price, round(quantity*0.6)))
        actions.append(format_action(to_stock, "SELL",to_price - 1, round(quantity*0.4)))

    return actions
      


