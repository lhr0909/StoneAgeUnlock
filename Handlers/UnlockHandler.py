import cyclone.web
import requests
from bs4 import BeautifulSoup

class UnlockHandler(cyclone.web.RequestHandler):

    def gotoURL(self, url, cookies=None, headers=None):
        r = requests.get(url, cookies=cookies, headers=headers)
        while int(r.headers["content-length"]) <= 3000:
            print "retrying URL %s..." % url
            r = requests.get(url, cookies=cookies, headers=headers)
        return r.text

    def post(self):
        base_url = "http://www.stoneage2.com.tw/"
        headers = {"User-Agent" : self.request.headers["User-Agent"]}
        
        unlock_url = base_url + self.get_argument("unlock_url", None)
        cookies = eval(self.get_argument("cookies", None))
        unlock_password = self.get_argument("unlock_password", None)

        unlock_page = self.gotoURL(unlock_url, cookies, headers)
        soup = BeautifulSoup(unlock_page)
        for input_box in soup.find_all("input"):
            if input_box.get("name") == "formhash":
                formhash = input_box.get("value")
                break

        verify_code = self.get_argument("verify_code", None)
        message_text = None
        while message_text == None:
            r = requests.post(unlock_url,
                data={
                    "formhash" : formhash,
                    "pwd" : unlock_password,
                    "cpwd" : verify_code,
                    "savesubmit" : "%E7%A2%BA+%E8%AA%8D"
                },
                cookies=cookies,
                headers=headers
            )
            message_text = BeautifulSoup(r.text).find(id="messagetext")
            
        self.write(message_text.find("p").get_text().encode('utf-8'))