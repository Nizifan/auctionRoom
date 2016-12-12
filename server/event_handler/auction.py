from common.message import MessageType
from server.memory import socket_mappings, room_mappings
from server.memory import user_id_mappings
from server.broadcast import broadcast



def run(sc, parameter):
    message_ = {
        "auctionname":{},
        "bid":{},
        "userlist":[]
    }

    for room in room_list:
        message_["auctionname"][room] = room_mappings["auctionname"][room]
        message_["bid"][room] = room_mappings["bid"][room]
        nickname_ = []
        for id in room_mappings["user_id"][room]:
            nickname_.append(user_id_mappings["nickname"][id])
        message_["userlist"][room] = nickname_

    message = {"message": message_}
    sc.socket.send(MessageType.leave,message)



