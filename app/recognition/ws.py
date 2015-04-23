from tornado import websocket
import json
from .cnn.classify import read

cl = []


class SocketHandler(websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        if self not in cl:
            cl.append(self)

    def on_message(self, message):
        gesture = json.loads(message)
        self.write_message(str(read(gesture)))

    def on_close(self):
        if self in cl:
            cl.remove(self)

    def get_compression_options(self):
        return {}
