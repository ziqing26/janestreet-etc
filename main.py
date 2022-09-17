#!/usr/bin/env python3
# ~~~~~==============   HOW TO RUN   ==============~~~~~
# 1) Configure things in CONFIGURATION section
# 2) Change permissions: chmod +x main.py
# 3) Run in loop: while true; do ./main.py --test prod-like; sleep 1; done

import argparse
from collections import deque
from enum import Enum
import time
import socket
import json

from adr import adr_action
from bond import bond_action
from xlf import xlf_action

# ~~~~~============== CONFIGURATION  ==============~~~~~
# Replace "REPLACEME" with your team name!
team_name = "TEAMNAME"

# ~~~~~============== MAIN LOOP ==============~~~~~

# You should put your code here! We provide some starter code as an example,
# but feel free to change/remove/edit/update any of it as you'd like. If you
# have any questions about the starter code, or what to do next, please ask us!
#
# To help you get started, the sample code below tries to buy BOND for a low
# price, and it prints the current prices for VALE every second. The sample
# code is intended to be a working example, but it needs some improvement
# before it will start making good trades!

SERVER_STATUS = 0
ORDER_ID = 0
orders, conversions = {}, {}

# Positions of symbols
symbol_pos = {
    "BOND": 0,
    "VALBZ": 0,
    "VALE": 0,
    "GS": 0,
    "MS": 0,
    "WFC": 0,
    "XLF": 0
}

# Books of symbols
symbol_book = {
    "BOND": {},
    "VALBZ": {},
    "VALE": {},
    "GS": {},
    "MS": {},
    "WFC": {},
    "XLF": {}
}

class Symbol(Enum):
  BOND: str = "BOND"
  GS: str = "GS"
  MS: str = "MS"
  USD: str = "USD"
  VALBZ: str = "VALBZ"
  VALE: str = "VALE"
  WFC: str = "WFC"
  XLF: str = "XLF"

def main():
    global ORDER_ID
    global symbol_book, symbol_pos

    args = parse_arguments()

    exchange = ExchangeConnection(args=args)

    # Store and print the "hello" message received from the exchange. This
    # contains useful information about your positions. Normally you start with
    # all positions at zero, but if you reconnect during a round, you might
    # have already bought/sold symbols and have non-zero positions.
    hello_message = exchange.read_message()
    print("First message from exchange:", hello_message)
    ORDER_ID = 0
    symbols = hello_message["symbols"]
    for symbol in symbols:
        symbol_pos[symbol["symbol"]] = symbol["position"]
    
    # Set up some variables to track the bid and ask price of a symbol. Right
    # now this doesn't track much information, but it's enough to get a sense
    # of the VALE market.
    vale_bid_price, vale_ask_price = None, None
    vale_last_print_time = time.time()

    # Here is the main loop of the program. It will continue to read and
    # process messages in a loop until a "close" message is received. You
    # should write to code handle more types of messages (and not just print
    # the message). Feel free to modify any of the starter code below.
    #
    # Note: a common mistake people make is to call write_message() at least
    # once for every read_message() response.
    #
    # Every message sent to the exchange generates at least one response
    # message. Sending a message in response to every exchange message will
    # cause a feedback loop where your bot's messages will quickly be
    # rate-limited and ignored. Please, don't do that!
    dic = {}
    while True:
        # exchange.send_add_message(order_id=ORDER_ID, symbol="BOND", dir="BUY", price=999, size=20)
        # orders[ORDER_ID] = ("BUY", "BOND", 999, 20)
        # ORDER_ID += 1
        # exchange.send_add_message(ORDER_ID, "BOND", "SELL", 1001, 20)
        # orders[ORDER_ID] = ("SELL", "BOND", 1001, 20)
        # ORDER_ID += 1
        message = exchange.read_message()
        # Some of the message types below happen infrequently and contain
        # important information to help you understand what your bot is doing,
        # so they are printed in full. We recommend not always printing every
        # message because it can be a lot of information to read. Instead, let
        # your code handle the messages and just print the information
        # important for you!
        if message["type"] == "close":
            print("The round has ended")
            break
        elif message["type"] == "error":
            print(message)
        elif message["type"] == "reject":
            print(message)
        elif message["type"] == "fill":
            print(message)
        elif message["type"] == "book":
            symbol = message["symbol"]
            buy = message["buy"]
            sell = message["sell"]

            # save order to book
            symbol_book[symbol] = { "BUY": buy, "SELL": sell }

            # Act on BOND transaction
            if symbol == "BOND":
                responses = bond_action(buy, sell)
                if responses:
                    for res in responses:
                        price = res["price"]
                        size = res["size"]
                        direction = res["dir"]
                        exchange.send_add_message(ORDER_ID, symbol, direction, price, size)
                        orders[ORDER_ID] = (direction, symbol, price, size)
                        ORDER_ID += 1
            
            # Act on VALE transaction
            if symbol == "VALE":
                # print("this is VALE", message)
                def best_price(side):
                    if message[side]:
                        return message[side][0][0]
                
                def best_price_qty(side):
                    if message[side]:
                        return message[side][0][1]

                vale_bid_price, vale_bid_qty = best_price("buy"), best_price_qty("buy")
                vale_ask_price, vale_ask_qty = best_price("sell"), best_price_qty("sell")
                
                # first = 1
                # now = time.time()
                # if first:
                #     vale_last_print_time = now
                #     first = 0

                # if now > vale_last_print_time + 1:
                #     vale_last_print_time = now
                print(
                    {
                        "vale_bid_price": vale_bid_price,
                        "vale_ask_price": vale_ask_price,
                    }
                )
                dic["vale_bid"] = [vale_bid_price, vale_bid_qty]
                dic["vale_ask"] = [vale_ask_price, vale_ask_qty] 

            # Act on VALBZ transaction
            if symbol == "VALBZ":
                # print("this is VALBZ", message)
                def best_price(side):
                    if message[side]:
                        return message[side][0][0]
                
                def best_price_qty(side):
                    if message[side]:
                        return message[side][0][1]

                valbz_bid_price, valbz_bid_qty = best_price("buy"), best_price_qty("buy")
                valbz_ask_price, valbz_ask_qty = best_price("sell"), best_price_qty("sell")
                
                # first = 1
                # now = time.time()
                # if first:
                #     valbz_last_print_time = now
                #     first = 0

                # if now > valbz_last_print_time + 1:
                #     valbz_last_print_time = now
                print(
                    {
                        "valbz_bid_price": valbz_bid_price,
                        "valbz_ask_price": valbz_ask_price,
                    }
                )
                dic["valbz_bid"] = [valbz_bid_price, valbz_bid_qty]
                dic["valbz_ask"] = [valbz_ask_price, valbz_ask_qty] 
            
            # if dic.get("valbz_bid") != None and dic.get("vale_bid") != None and dic.get("valbz_bid")[0] and dic.get("vale_bid")[0]:
            #     responses = adr_action(dic, symbol_pos)

            #     if responses:
            #         for res in responses:
            #             _type =  res["type"]
            #             size = res["size"]
            #             direction = res["dir"]
            #             symbol = res["symbol"]
            #             if _type == "ADD":
            #                 price = res["price"]
            #                 exchange.send_add_message(ORDER_ID, symbol, direction, price, size)
            #                 orders[ORDER_ID] = (direction, symbol, price, size)
            #                 # print("ORDERS in if", orders)
            #             else:
            #                 exchange.send_convert_message(ORDER_ID, symbol, direction, size)
            #                 conversions[ORDER_ID] = (direction, symbol, size)
            #                 # print("CONVERSIONS in else", conversions)

            #             ORDER_ID += 1
              
            # Act on XLF transaction
            if message["symbol"] == "XLF":
                responses = xlf_action(symbol_book["BOND"], symbol_book["GS"],
                                symbol_book["MS"], symbol_book["WFC"],
                                symbol_book["XLF"])
                if responses:
                    for response in responses:
                        response["order_id"] = ORDER_ID
                        type_res = response["type"]
                        if type_res == "ADD":
                            exchange.send_add_message(ORDER_ID, response["symbol"], response["dir"], response["price"], response["size"])
                        elif type_res == "CONVERT":
                            exchange.send_convert_message(ORDER_ID, response["symbol"], response["dir"], response["size"])

                        if type_res != "CONVERT":
                            orders[ORDER_ID] = (response["dir"], response["symbol"], response["price"], response["size"])
                            if response["dir"] == "BUY":
                                symbol_pos["USD"] = symbol_pos["USD"] - (response["price"] * response["size"])
                        else:
                            conversions[ORDER_ID] = (response["dir"], response["symbol"], response["size"])
                        ORDER_ID += 1


        elif message["type"] == "ack":  
            _order_id = message["order_id"]
            if _order_id in orders:
                order = orders[_order_id]
                print("Order {}: Dir - {}, Symbol - {}, Price - {}, Size - {} has been entered into the books"
                        .format(_order_id, order[0], order[1], order[2], order[3]))
            else:
                # print("CONVERSIONS", conversions)
                # print("order_id", _order_id)
                conversion = conversions[_order_id]
                print("Order {}: Dir - {}, Symbol - {}, Size - {} has been converted"
                        .format(_order_id, conversion[0], conversion[1], conversion[2]))
                if conversion[1] == str(Symbol.VALE):
                    symbol_pos[str(Symbol.VALE)] += conversion[2]
                    symbol_pos[str(Symbol.VALBZ)] -= conversion[2]
                    symbol_pos[str(Symbol.USD)] -= 10
                elif conversion[1] == str(Symbol.VALBZ):
                    symbol_pos[str(Symbol.VALE)] -= conversion[2]
                    symbol_pos[str(Symbol.VALBZ)] += conversion[2]
                    symbol_pos[str(Symbol.USD)] -= 10
                elif conversion[1] == str(Symbol.XLF):
                    if conversion[0] == "BUY":
                        symbol_pos[str(Symbol.BOND)] -= 3
                        symbol_pos[str(Symbol.GS)] -= 2
                        symbol_pos[str(Symbol.MS)] -= 3
                        symbol_pos[str(Symbol.WFC)] -= 2
                        symbol_pos[str(Symbol.XLF)] += 10
                    elif conversion[0] == "SELL":
                        symbol_pos[str(Symbol.BOND)] += 3
                        symbol_pos[str(Symbol.GS)] += 2
                        symbol_pos[str(Symbol.MS)] += 3
                        symbol_pos[str(Symbol.WFC)] += 2
                        symbol_pos[str(Symbol.XLF)] -= 10
                    symbol_pos[str(Symbol.USD)] -= 100

                print("CURRENT POSITION: {}".format(symbol_pos))

        
            time.sleep(0.1)



# ~~~~~============== PROVIDED CODE ==============~~~~~

# You probably don't need to edit anything below this line, but feel free to
# ask if you have any questions about what it is doing or how it works. If you
# do need to change anything below this line, please feel free to


class Dir(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


class ExchangeConnection:
    def __init__(self, args):
        self.message_timestamps = deque(maxlen=500)
        self.exchange_hostname = args.exchange_hostname
        self.port = args.port
        exchange_socket = self._connect(add_socket_timeout=args.add_socket_timeout)
        self.reader = exchange_socket.makefile("r", 1)
        self.writer = exchange_socket

        self._write_message({"type": "hello", "team": team_name.upper()})

    def read_message(self):
        """Read a single message from the exchange"""
        message = json.loads(self.reader.readline())
        if "dir" in message:
            message["dir"] = Dir(message["dir"])
        return message

    def send_add_message(
        self, order_id: int, symbol: str, dir: Dir, price: int, size: int
    ):
        """Add a new order"""
        self._write_message(
            {
                "type": "add",
                "order_id": order_id,
                "symbol": symbol,
                "dir": dir,
                "price": price,
                "size": size,
            }
        )

    def send_convert_message(self, order_id: int, symbol: str, dir: Dir, size: int):
        """Convert between related symbols"""
        self._write_message(
            {
                "type": "convert",
                "order_id": order_id,
                "symbol": symbol,
                "dir": dir,
                "size": size,
            }
        )

    def send_cancel_message(self, order_id: int):
        """Cancel an existing order"""
        self._write_message({"type": "cancel", "order_id": order_id})

    def _connect(self, add_socket_timeout):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if add_socket_timeout:
            # Automatically raise an exception if no data has been recieved for
            # multiple seconds. This should not be enabled on an "empty" test
            # exchange.
            s.settimeout(5)
        s.connect((self.exchange_hostname, self.port))
        return s

    def _write_message(self, message):
        # print("We are writing: ", message)
        what_to_write = json.dumps(message)
        if not what_to_write.endswith("\n"):
            what_to_write = what_to_write + "\n"

        length_to_send = len(what_to_write)
        total_sent = 0
        while total_sent < length_to_send:
            sent_this_time = self.writer.send(
                what_to_write[total_sent:].encode("utf-8")
            )
            if sent_this_time == 0:
                raise Exception("Unable to send data to exchange")
            total_sent += sent_this_time

        now = time.time()
        self.message_timestamps.append(now)
        if len(
            self.message_timestamps
        ) == self.message_timestamps.maxlen and self.message_timestamps[0] > (now - 1):
            print(
                "WARNING: You are sending messages too frequently. The exchange will start ignoring your messages. Make sure you are not sending a message in response to every exchange message."
            )


def parse_arguments():
    test_exchange_port_offsets = {"prod-like": 0, "slower": 1, "empty": 2}

    parser = argparse.ArgumentParser(description="Trade on an ETC exchange!")
    exchange_address_group = parser.add_mutually_exclusive_group(required=True)
    exchange_address_group.add_argument(
        "--production", action="store_true", help="Connect to the production exchange."
    )
    exchange_address_group.add_argument(
        "--test",
        type=str,
        choices=test_exchange_port_offsets.keys(),
        help="Connect to a test exchange.",
    )

    # Connect to a specific host. This is only intended to be used for debugging.
    exchange_address_group.add_argument(
        "--specific-address", type=str, metavar="HOST:PORT", help=argparse.SUPPRESS
    )

    args = parser.parse_args()
    args.add_socket_timeout = True

    if args.production:
        args.exchange_hostname = "production"
        args.port = 25000
    elif args.test:
        args.exchange_hostname = "test-exch-" + team_name
        args.port = 25000 + test_exchange_port_offsets[args.test]
        if args.test == "empty":
            args.add_socket_timeout = False
    elif args.specific_address:
        args.exchange_hostname, port = args.specific_address.split(":")
        args.port = int(port)

    return args


if __name__ == "__main__":
    # Check that [team_name] has been updated.
    main()
