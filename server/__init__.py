#!/usr/bin/env python
#-*- coding: UTF-8 -*-  
import socket
from common.config import get_config
from common.transmission.secure_channel import accept_client_to_secure_channel
from server.event_handler import handle_event
from server.memory import socket_mappings, remove_from_socket_mapping, connections, user_id_mappings, room_list
import server.memory
from common.message import MessageType
from server.broadcast import broadcast
import select
from server.memory import room_mappings
import _thread

COMMAND = ['/msg', '/list', '/kickout', '/enter', '/leave', ]

def run():
    config = get_config()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((config['server']['bind_ip'], config['server']['bind_port']))
    s.listen(1)

    self.room = -1

    openauction(1,"caiyihan de pants", 100)

    print("Server listening on " + config['server']['bind_ip'] + ":" + str(config['server']['bind_port']))

    _thread.start_new_thread(mainLoop, ())

    while True:
        rlist, wlist, xlist = select.select(connections + [s], [], [])

        for i in rlist:

            if i == s:
                # 监听socket为readable，说明有新的客户要连入
                sc = accept_client_to_secure_channel(s)
                socket_mappings['sc'][sc.socket] = sc
                socket_mappings['user_id'][sc.socket] = server.memory.user_id_incr
                server.memory.user_id_incr += 1
                connections.append(sc.socket)

                continue

            # 如果不是监听socket，就是旧的客户发消息过来了
            sc = socket_mappings['sc'][i]

            try:
                data = sc.recv()
            except socket.error:
                data = ""

            if data:
                handle_event(sc, data['type'], data['parameters'])

            else:
                # Connection closed
                i.close()
                connections.remove(i)
                broadcast(MessageType.on_user_offline, socket_mappings['user_id'][i])
                remove_from_socket_mapping(i)

def mainLoop():
    while True:
        msg = input().split(' ');
        if msg[0] not in COMMAND:
            print('Wrong input,try again')
            continue
        if msg[0] == '/msg':
            if len(msg) == 2:
                broadcast(MessageType.msg, msg[1])
            else:
                socket = user_id_mappings['sc'][int(msg[1])]
                socket.send(MessageType.msg, msg[2])
        if msg[0] == '/list':
            if self.room == -1:
                print("Not in room")
                continue
            for id in room_mappings[self.room]:
                print(user_id_mappings['nickname'][id])
        if msg[0] == '/kickout':
            socket = user_id_mappings['sc'][int(msg[1])]
            socket.send(MessageType.kickout, "")
        if msg[0] == '/openauction':
            openauction(msg[1],msg[2],msg[3])
        if msg[0] == '/auction':
            for room in room_list:
                print(room + room_mappings['auctionname'] + room['bid'])
        if msg[0] == '/enter':
            if formatcheck(msg, 2):
                continue
            if self.room != -1:
                print("already in room")
                continue
            self.room = msg[1]

        if msg[0] == '/leave':
            self.room = -1

        if msg[0] == '/close':
            room_mappings.remove(msg[1])
            for id in room_mappings['user_id']:
                socket = user_id_mappings['sc'][id]
                socket.send(MessageType.close,"")

def openauction(roomnumber,auctionname,bidprice):
    room_mappings['user_id'][roomnumber] = []
    room_mappings['auctionname'] = auctionname
    room_mappings['bid'] = bidprice
    room_mappings['lastbidder'] = -1
    room_list.append(roomnumber)
    print("open auction successfully")

def formatcheck(msg,param):
    if len(msg) != param:
        print("Param wrong!")
        return 1
    else:
        return 0