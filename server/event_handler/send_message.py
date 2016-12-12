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
        message_ = "you have enter room" + str(parameter) + 'successfully'
        entered_ = parameter
        socket_mappings['room'][sc.socket] = parameter
        user_id = socket_mappings["user_id"][sc.socket]
        room_mappings["user_id"][parameter].append(user_id)

    else:
        message_ = "The room doesn't exist"
        entered_ = 0
    message = {"message": message_, "enter": str(entered_)}
    broadcast(MessageType.on_new_message,message)



