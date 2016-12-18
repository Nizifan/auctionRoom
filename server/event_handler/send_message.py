from pprint import pprint
from common.message import MessageType
from server.memory import socket_mappings
from server.memory import user_id_mappings
from server.memory import room_mappings
from server.memory import room_list
import server.memory
from server.memory import get_online_users
from server.broadcast import broadcast
import time


def run(sc, parameter):
    if parameter in room_list:
        entered_ = parameter
        socket_mappings['room'][sc.socket] = parameter
        user_id = socket_mappings["user_id"][sc.socket]
        room_mappings["user_id"][parameter].append(user_id)
        bidder = room_mappings["lastbidder"][str(parameter)]
        nickname = socket_mappings["nickname"][sc.socket]
        if bidder == -1:
            bidder_name = "System initial"
        else:
            bidder_name = user_id_mappings["nickname"][bidder]
        price = room_mappings['bid'][parameter]
        auction = room_mappings["auctionname"][parameter]
        message = {"enter": entered_, "bid": price, "lastbidder": bidder_name, "user_name":nickname,"auctionname":auction}
        broadcast(MessageType.on_new_message, message)

    else:
        entered_ = -1
        price = 0
        bidder_name = ""
        message = {"enter": entered_}
        sc.send(MessageType.on_new_message,message)





