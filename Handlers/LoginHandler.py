import cyclone.web
import requests
from bs4 import BeautifulSoup

class LoginHandler(cyclone.web.RequestHandler):

    def gotoURL(self, url, cookies=None, headers=None):
        r = requests.get(url, cookies=cookies, headers=headers)
        while int(r.headers["content-length"]) <= 3000:
            print "retrying URL %s..." % url
            r = requests.get(url, cookies=cookies, headers=headers)
        return r.text

    def post(self):
        base_url = "http://www.stoneage2.com.tw/"
        headers = {"User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.65 Safari/537.36"}
        
        username = self.get_argument("username", None)
        password = self.get_argument("password", None)

        r1 = requests.post(base_url + 'member.php?ac=login', 
            data={
                "formhash" : "f94c7df0", 
                "username" : username,
                "pwd" : password,
                "loginsubmit" : "+"
            },
            headers=headers
        )
        cookies = requests.utils.dict_from_cookiejar(r1.cookies)

        locked_accounts = []
        gamer_list = self.gotoURL(base_url + 'member.php?ac=gamerlist', cookies, headers)
        soup_list = BeautifulSoup(gamer_list)
        for link in soup_list.find_all("a"):
            href = link.get("href")
            if href.startswith("member.php?ac=unlock&u="):
                unlock_page = self.gotoURL(base_url + href, cookies, headers)
                soup_unlock = BeautifulSoup(unlock_page)
                for img in soup_unlock.find_all("img"):
                    src = img.get("src")
                    if src.startswith("verifycode.php?t="):
                        img_raw = requests.get(base_url + src, cookies=cookies, headers=headers)
                        locked_accounts.append((href, img_raw.content.encode('hex_codec')))
                        break
        self.render("login.html", locked_accounts=locked_accounts)