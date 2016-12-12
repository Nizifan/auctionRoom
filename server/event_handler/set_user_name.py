from pprint import pprint
from common.message import MessageType
from server.memory import socket_mappings
from server.memory import user_id_mappings
from server.memory import get_online_users
from server.broadcast import broadcast
import server.memory


def run(sc, parameter):
    # 如果昵称已经被占用，提醒用户换一个
    for key, value in socket_mappings['nickname'].items():
        if value == parameter:
            sc.send(MessageType.err_nickname_taken)
            return

    socket_mappings['nickname'][sc.socket] = parameter
    user_id_mappings['sc'][socket_mappings['user_id'][sc.socket]] = sc
    user_id_mappings['nickname'][socket_mappings['user_id'][sc.socket]] = parameter
    sc.send(MessageType.set_name_successful, socket_mappings['user_id'][sc.socket])
    sc.send(MessageType.notify_online_user_list, get_online_users())

