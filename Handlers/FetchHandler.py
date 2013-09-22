import cyclone.web
import requests
from bs4 import BeautifulSoup

class FetchHandler(cyclone.web.RequestHandler):

    def post(self, timestamp):
        base_url = "http://www.stoneage2.com.tw/"
        headers = {"User-Agent" : self.request.headers["User-Agent"]}

        cookies = eval(self.get_argument("cookies", None))
        fetch_url = base_url + "verifycode.php?t=" + timestamp
        print cookies

        img_raw = requests.get(fetch_url, cookies=cookies, headers=headers)
        self.write(img_raw.content.encode('hex_codec'))