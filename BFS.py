import requests
from bs4 import BeautifulSoup
import json
import time
import math

class Person(object):
    def __init__(self, urlToken):
        self.urlToken = urlToken
        self.follower_count = 0
        self.follower = set()
        self.following_count = 0
        self.following = set()
        self.profile_url = "https://www.zhihu.com/people/" + self.urlToken + "/following"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36',
            "Host": "www.zhihu.com",
            "Referer": "https://www.zhihu.com/",
        }
        self.success_code = 200
        self.following_per_page = 20
        self.follower_per_page = 20


    def get_pagejson(self, url):
        try:
            response = requests.get(url, headers=self.headers)

            if response.status_code == self.success_code:
                soup = BeautifulSoup(response.text, 'html.parser')
                pagejson_text = soup.body.contents[1].attrs['data-state']
                pagejson = json.loads(pagejson_text)
            else:
                pagejson = dict()
        except:
            pagejson = dict()
        return pagejson

    def update_following(self):
        start_page = self.get_pagejson(self.profile_url)
        self.following_count = start_page['entities']['users'][self.urlToken]['followingCount']
        self.following_max_page = math.ceil(self.following_count / self.following_per_page)
        print("%s has followed %d people." % (self.urlToken, self.following_count))
        print("It will take approximately %d s to finish updating." % (self.following_max_page // 2))
        for i in range(1, self.following_max_page+1):
            url = self.profile_url + "?page=" + str(i)
            page = self.get_pagejson(url)
            print(page)
            for key in page['entities']['users']:
                self.following.add(key)
            time.sleep(0.5)

    def update_follower(self):
        start_page = self.get_pagejson(self.profile_url)
        self.follower_count = start_page['entities']['users'][self.urlToken]['followerCount']
        self.follower_max_page = math.ceil(self.follower_count / self.follower_per_page)
        print("%s is followed by %d people." % (self.urlToken, self.follower_count))
        print("It will take approximately %d s to finish updating." % (self.follower_max_page // 2))
        for i in range(1, self.follower_max_page + 1):
            url = self.profile_url + "?page=" + str(i)
            page = self.get_pagejson(url)
            for key in page['entities']['users']:
                self.follower.add(key)
            time.sleep(0.5)
            print(self.follower)

    def update_college(self):
        pass

    def update_career(self):
        pass

    def update_(self):
        pass

Person("excited-vczh").update_following()
