# from main import *
# def convert(from_stock, to_tock, quantity):
#     pass

# def actions(bond, quantity, price):
#     pass


def format_action(symbol, direction, price, size):
    return {"type": "add","symbol": symbol, "dir": direction, "price": price, "size": size}

def convert(from_stock, to_stock, size):
    return {"type": "convert", "order_id": 0, "symbol": to_stock, "dir": "BUY", "size": size}

def adr_action(trade_info):
    actions = []
    if trade_info["valbz_bid"][0] > trade_info["vale_ask"][0] + 2:
        print("I am here")
        from_stock = "VALE"
        from_price = trade_info["vale_ask"][0]
        to_stock = "VALBZ"
        to_price = trade_info["valbz_bid"][0]
        quantity = trade_info["vale_ask"][1]

        actions.append(format_action(from_stock, "BUY", from_price, quantity))
        actions.append(convert(from_stock, to_stock, quantity))
        actions.append(format_action(to_stock, "SELL",to_price, quantity))


    if trade_info["vale_bid"][0] > trade_info["valbz_ask"][0] + 2:
        print("I am here")
        from_stock = "VALBZ"
        from_price = trade_info["valbz_ask"][0]
        to_stock = "VALE"
        to_price = trade_info["valbz_bid"][0]
        quantity = trade_info["valbz_ask"][1]

        actions.append(format_action("add", "BUY", from_stock, from_price, quantity))
        actions.append(convert(from_stock, to_stock, quantity))
        actions.append(format_action("add", "SELL", to_stock, to_price, quantity))

    return actions
      


