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
    sender_user_id = socket_mappings['user_id'][sc.socket]
    nickname_ = user_id_mappings['nickname'][sender_user_id]
    room = socket_mappings['room'][sc.socket]
    bid_price_ = room_mappings['bid'][room]
    if bid_price_ < int(parameter):
        message_ = " has bid " + str(parameter)
        room_mappings['bid'][room] = int(parameter)
        room_mappings['lastbidder'][room] = sender_user_id
        message = {"message": message_, "nickname": nickname_, "roomnumber":room, 'bid':parameter}
    else:
        message_ = ""
        message = {"message": message_, "nickname": nickname_, "roomnumber": room, 'bid': bid_price_}
    broadcast(MessageType.bid,message)