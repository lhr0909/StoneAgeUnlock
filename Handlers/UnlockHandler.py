import cyclone.web

class UnlockHandler(cyclone.web.RequestHandler):

    def get(self):
        self.render("index.html")