from common.transmission.secure_channel import establish_secure_channel_to_server
from common.message import MessageType
from pprint import pprint
from client.memory import user_list
from client.memory import current_user
import select
import datetime
import time
import _thread



COMMAND = [ '/bid','/enter','/leave', '/auctions', '/list']

class ChatRoom():
    def __init__(self):
        self.sc = establish_secure_channel_to_server()
        self.should_exit = False

        self.room = -1

        self.send_name()

        while True:
            rlist, wlist, xlist = select.select([self.sc.socket], [self.sc.socket], [])

            if (self.should_exit):
                return

            if len(rlist):
                data = self.sc.recv()
                if data:
                    if data['type'] == MessageType.set_name_successful:
                        current_user['id'] = data['parameters']
                        print("set name successfully,your id:"+str(data['parameters']))
                        current_user['nickname'] = self.name

                    if data['type'] == MessageType.err_nickname_taken:
                        print("Your name has been taken")
                        self.send_name()

                    if data['type'] == MessageType.notify_online_user_list:
                        for user in data['parameters']:
                            user_list[user['id']] = user
                        self.should_exit = True
                        _thread.start_new_thread(self.socket_reader, ())
                        self.mainLoop()

    def mainLoop(self):
        while True:
            msg = input().split(' ');
            if msg[0] not in COMMAND:
                print('Wrong input,try again')
                continue
            if msg[0] == '/enter':
                if self.room != -1:
                    print('you should exit first')
                    continue
                self.sc.send(MessageType.send_message,msg[1])
            if msg[0] == '/leave':
                if self.room == -1:
                    print('you are not in room')
                    continue
                self.sc.send(MessageType.leave,self.room)
            if msg[0] == '/bid':
                if self.room == -1:
                    print('you are not in room')
                    continue
                self.sc.send(MessageType.bid, msg[1])
            if msg[0] == '/auctions':
                self.sc.send(MessageType.auction)
            if msg[0] == '/list':
                self.sc.send(MessageType.list)



    def insert_system_message(self, message, hide_time=False):
        if hide_time:
            time_message = ''
        else:
            time_message = datetime.datetime.fromtimestamp(
                time.time()
            ).strftime('%Y-%m-%d %H:%M:%S')

        print('[系统消息]  ' + message + ' ' + time_message + ' ' + ' \n')
        return

    def send_name(self):
        print("please input your name")
        self.name = input()
        while self.name == '':
            print("name can't be blank")
            print("please input your name")
            self.name = input()
        print(MessageType.set_user_name)
        self.sc.send(MessageType.set_user_name, self.name)

    def socket_reader(self):
        while True:
            rlist, wlist, xlist = select.select([self.sc.socket], [self.sc.socket], [])

            if len(rlist):
                data = self.sc.recv()
                if data:
                    if data['type'] == MessageType.on_user_online:
                        user_list[data['parameters']['id']] = data['parameters']
                        self.insert_system_message(data['parameters']['nickname'] + ' 已经上线')

                    if data['type'] == MessageType.on_user_offline:
                        self.insert_system_message(data['parameters'] + ' 已经离线')

                    if data['type'] == MessageType.auction:
                        message_ = data['parameters']['message']
                        for key in range(len(message_['bid'])):
                            key = str(key+1)
                            print("=========auction room" + key + "========")
                            print("auction name:" + message_['auctionname'][key])
                            print("bid price:" + str(message_['bid'][key]))
                            print("user:")
                            pprint(message_['userlist'][key])

                    if data['type'] == MessageType.list:
                        print("bidder in the room:")
                        pprint(data['parameters'])

                    if data['type'] == MessageType.on_new_message:
                        if data['parameters']["enter"] == -1:
                            print("The room doesn't exist")
                        elif self.name == data['parameters']['user_name']:
                            print("You entered room " + str(data['parameters']["enter"]) + " successfully")
                            print("room info:")
                            print("auction name:" + data['parameters']["auctionname"])
                            print("bid price:" + str(data['parameters']["bid"]) )
                            print("last bidder:" + data['parameters']["lastbidder"])
                            self.room = data['parameters']["enter"]
                        elif self.room == data['parameters']["enter"]:
                            print( data['parameters']['user_name'] + " entered room")

                    if data['type'] == MessageType.leave:
                        if data['parameters']['nickname'] == self.name:
                            if data['parameters']['leave'] == '0':
                                print("You are the last bidder")
                                print("last bidder can't leave")
                            else:
                                print("You have left room")
                                self.room = -1
                            continue

                        if self.room == data['parameters']['roomnumber']:
                            print(data['parameters']['nickname'] + " has left room")

                    if data['type'] == MessageType.bid:
                        if data['parameters']['message'] == '':
                            if data['parameters']['nickname'] == self.name:
                                print("You can't bet price lower" )
                                print("the price now is " + str(data['parameters']['bid']))
                            continue

                        if data['parameters']['nickname'] == self.name:
                            nickname_ = 'You '
                        else:
                            nickname_ = data['parameters']['nickname']

                        if self.room == data['parameters']['roomnumber']:
                            print(nickname_ + data['parameters']['message'])

                    if data['type'] == MessageType.msg:
                        self.insert_system_message(data['parameters'])

                    if data['type'] == MessageType.kickout:
                        self.room = -1
                        self.insert_system_message("你被管理员踢出了房间，嘻嘻")

                    if data['type'] == MessageType.close:
                        self.room = -1
                        self.insert_system_message("The room has been shut down")
                        self.insert_system_message("You are at lobby now")


                else:
                    print('服务器已被关闭')


