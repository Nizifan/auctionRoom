from common.message import MessageType
from server.memory import socket_mappings
from server.memory import user_id_mappings
from server.broadcast import broadcast



def run(sc, parameter):
    sender_user_id = socket_mappings['user_id'][sc.socket]

    message = {"message": message_, "nickname": nickname_, "roomnumber":str(parameter)}
    broadcast(MessageType.leave,message)



