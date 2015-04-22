#!/usr/bin/env python

import os
from app import app, server
from tornado.ioloop import IOLoop

if __name__ == "__main__":
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    server.listen(port)
    IOLoop.instance().start()
