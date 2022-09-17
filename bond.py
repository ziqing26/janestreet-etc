THRESHOLD = 1000

def format_action(direction, price, size):
    return {"symbol": "BOND", "dir": direction, "price": price, "size": size}

def bond_action(buy, sell):
    actions = []
    for i in range(len(buy)):
        if buy[i][0] > THRESHOLD:
            actions.append(format_action("SELL", buy[i][0], buy[i][1]))
    for i in range(len(sell)):
        if sell[i][0] < THRESHOLD:
            actions.append(format_action("BUY", sell[i][0], sell[i][1]))
    return actions
