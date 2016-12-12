from common.message import MessageType
from server.memory import socket_mappings,room_mappings
from server.memory import user_id_mappings
from server.broadcast import broadcast



def run(sc, parameter):
    sender_user_id = socket_mappings['user_id'][sc.socket]
    nickname_ = user_id_mappings['nickname'][sender_user_id]
    room_mappings['user_id'][str(parameter)].remove(sender_user_id)
    message_ = " has left room"

    message = {"message": message_, "nickname": nickname_, "roomnumber":str(parameter)}
    broadcast(MessageType.leave,message)



