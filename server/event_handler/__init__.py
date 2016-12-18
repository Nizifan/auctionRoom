from pprint import pprint
import server.event_handler.set_user_name
import server.event_handler.send_message
import server.event_handler.leave
import server.event_handler.bid
import server.event_handler.auction
import server.event_handler.list

from common.message import MessageType

event_handler_map = {
    MessageType.set_user_name: set_user_name,
    MessageType.send_message: send_message,
    MessageType.leave: leave,
    MessageType.bid: bid,
    MessageType.auction: auction,
    MessageType.list: list

}


def handle_event(sc, event_type, parameters):
    event_handler_map[event_type].run(sc, parameters)
