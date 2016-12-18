from common.message import MessageType
from server.memory import socket_mappings, room_mappings
from server.memory import user_id_mappings
from server.broadcast import broadcast



def run(sc, parameter):

    room = socket_mappings["room"][sc.socket]

    nickname_ = []
    for id in room_mappings["user_id"][room]:
        nickname_.append(user_id_mappings["nickname"][id])
    sc.send(MessageType.list,nickname_)



