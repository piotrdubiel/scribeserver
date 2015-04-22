from tornado import websocket, web
from app import app

cl = []


class SocketHandler(websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        if self not in cl:
            cl.append(self)

    def on_message(self, message):
        print message

    def on_close(self):
        if self in cl:
            cl.remove(self)

#sockets = Sockets(app)

#@sockets.route("/ws/recognize")
#def recognize(ws):
#    while True:
#        try:
#            message = ws.receive()
#            print message
#        except WebSocketError:
#            pass
