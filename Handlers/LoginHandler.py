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
        headers = {"User-Agent" : self.request.headers["User-Agent"]}
        
        username = self.get_argument("username", None)
        password = self.get_argument("password", None)
        wrong_password = False

        login_url = base_url + 'member.php?ac=login'
        login_page = requests.get(login_url, headers=headers).text
        soup = BeautifulSoup(login_page)
        for input_box in soup.find_all("input"):
            if input_box.get("name") == "formhash":
                formhash = input_box.get("value")
                break

        r = requests.post(login_url, 
            data={
                "formhash" : formhash, 
                "username" : username,
                "pwd" : password,
                "loginsubmit" : "+"
            },
            headers=headers
        )
        cookies = requests.utils.dict_from_cookiejar(r.cookies)
        if "aege_taozhu_auth" not in cookies:
            wrong_password = True
            self.render("login.html", wrong_password=wrong_password)
            return

        locked_accounts = []
        gamer_list = self.gotoURL(base_url + 'member.php?ac=gamerlist', cookies, headers)
        soup_list = BeautifulSoup(gamer_list)
        for link in soup_list.find_all("a"):
            href = link.get("href")
            if href.startswith("member.php?ac=unlock&u="):
                locked_accounts.append(href)
        self.render("login.html", locked_accounts=locked_accounts, cookies=str(cookies), wrong_password=wrong_password)