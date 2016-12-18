from common.message import MessageType
from server.memory import socket_mappings,room_mappings
from server.memory import user_id_mappings
from server.broadcast import broadcast



def run(sc, parameter):
    sender_user_id = socket_mappings['user_id'][sc.socket]
    nickname_ = user_id_mappings['nickname'][sender_user_id]

    #print(room_mappings['lastbidder'][str(parameter)])

    if room_mappings['lastbidder'][str(parameter)] == nickname_:
        sc.send(MessageType.leave, {"leave":"0", "nickname":nickname_})
    else:
        if sender_user_id in room_mappings['user_id'][str(parameter)]:
            room_mappings['user_id'][str(parameter)].remove(sender_user_id)
        message = {"leave": "1", "nickname": nickname_, "roomnumber":str(parameter)}
        broadcast(MessageType.leave,message)



