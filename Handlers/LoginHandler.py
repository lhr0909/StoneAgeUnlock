import cyclone.web

class LoginHandler(cyclone.web.RequestHandler):

    def get(self):
        self.render("index.html")