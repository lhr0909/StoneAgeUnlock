import os, sys, cyclone.web
from twisted.python import log
from twisted.internet import reactor
from Handlers import IndexHandler, UnlockHandler, LoginHandler

class Application(cyclone.web.Application):
    def __init__(self):
        handlers = [
            (r"/", IndexHandler.IndexHandler),
            (r"/login", LoginHandler.LoginHandler),
            (r"/unlock/(.*)", UnlockHandler.UnlockHandler),
        ]

        settings = {
            "debug": True,
            "static_path": "./static",
            "template_path": "./template",
            }

        cyclone.web.Application.__init__(self,
            handlers, **settings)

if __name__ == "__main__":
    log.startLogging(sys.stdout)
    port = int(os.environ.get('PORT', 5000))
    reactor.listenTCP(port, Application())
    reactor.run()