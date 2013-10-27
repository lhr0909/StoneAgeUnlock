#! /usr/local/bin/python
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
# from PIL import Image
from getpass import getpass
from time import time, sleep

cardnos = []

def gotoURL(url, cookies=None, headers=None):
    r = requests.get(url, cookies=cookies, headers=headers)
    # print r.status_code
    # print r.headers
    while int(r.headers["content-length"]) <= 3000:
        print "retrying URL %s..." % url
        r = requests.get(url, cookies=cookies, headers=headers)
    return r.text

def put_gift(url, cardno, cookies, headers):
    r = requests.post(url, cookies=cookies, headers=headers)
    soup =  BeautifulSoup(r.text)
    for input_box in soup.find_all("input"):
        if input_box.get("name") == "formhash":
            formhash = input_box.get("value")
        elif input_box.get("name") == "timehash":
            timehash = input_box.get("value")
    print "putting " + cardno + "..."
    r = requests.post(url,
        data={
            "formhash" : formhash,
            "timehash" : timehash,
            "pid" : "332355",
            "sid" : "1",
            "cardno" : cardno,
            "savesubmit" : "%E7%A2%BA+%E8%AA%8D"
        },
        cookies=cookies,
        headers=headers
    )
    print r.status_code
    print r.headers
    print BeautifulSoup(r.text).get_text().encode('utf-8')

base_url = "http://www.stoneage.tw/"
headers = {"User-Agent" : "Hi"}

username = raw_input("Username: ")
password = getpass("Login Password: ")

print "Logging in..."

login_url = base_url + 'member.php?ac=login'
login_page = requests.get(login_url, headers=headers).text
soup = BeautifulSoup(login_page)
for input_box in soup.find_all("input"):
    if input_box.get("name") == "formhash":
        formhash = input_box.get("value")
        break

r1 = requests.post(base_url + 'member.php?ac=login', 
    data={
        "formhash" : formhash, 
        "username" : username,
        "pwd" : password,
        "loginsubmit" : "+"
    },
    headers=headers
)
cookies = requests.utils.dict_from_cookiejar(r1.cookies)
# print r1.text.encode('utf-8')
# print r1.status_code
# print r1.headers
print requests.utils.dict_from_cookiejar(r1.cookies)
gift_url = base_url + 'member.php?ac=gift'
for cardno in cardnos:
    sleep(1)
    put_gift(gift_url, cardno, cookies, headers)

print "finished"

