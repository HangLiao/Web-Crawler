import requests
import http.cookiejar
import re
import json
import time

class Login(object):

    # store global variables
    def __init__(self):
        self.headers = {
            'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 '
                           '(KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36',
            'Host' : 'www.zhihu.com',
            'Referer' : 'https://www.zhihu.com'
        }
        self.session = requests.session()
        self.session.cookies = http.cookiejar.LWPCookieJar("cookie")
        self.success_code = 200
        self.r = 1000       # used to construct the captcha url
        self.url = "https://www.zhihu.com"
        self.profile_url = "https://www.zhihu.com/settings/profile"
        self.phone_login_url = "http://www.zhihu.com/login/phone_num"
        self.computer_login_url = "https://www.zhihu.com/login/email"

    def main(self):
        try:
            self.session.cookies.load(ignore_discard=True)
        except IOError:
            print("No Cookies Found")

        if self.isLogin():
            print("Already logged in")
        else:
            username = input('please type your Zhihu username:')
            pw = input('please type your Zhihu password:')
            self.login(username, pw)

    def isLogin(self):
        url = self.profile_url
        message = self.session.get(url, headers=self.headers, allow_redirects=False)
        status = message.status_code
        return status == self.success_code

    def login(self, username, pw):
        session = self.session
        headers = self.headers

        if re.match(r'\d{11}$', username):
            url = self.phone_login_url
            data = {'_xsrf': self.get_xsrf(),
                    'password': pw,
                    'remember_me': 'true',
                    'phone_num': username
                    }
        else:
            url = self.computer_login_url
            data = {'_xsrf': self.get_xsrf(),
                    'password': pw,
                    'remember_me': 'true',
                    'email': username
                    }

        result = session.post(url, data=data, headers=headers)
        if (json.loads(result.text))["r"] == 1: #login failed
            data['captcha'] = self.get_captcha()
            result = session.post(url, data=data, headers=headers)
            print((json.loads(result.text))['msg'])
        session.cookies.save(ignore_discard=True, ignore_expires=True)

    def get_xsrf(self):
        response = self.session.get(self.url, headers=self.headers)
        html = response.text
        get_xsrf_pattern = re.compile(r'<input type="hidden" name="_xsrf" value="(.*?)"')
        _xsrf = re.findall(get_xsrf_pattern, html)[0]
        return _xsrf

    def get_captcha(self):
        t = str(int(time.time() * self.r))      # Is this the real way website generate their captcha??
        captcha_url = 'http://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
        response = self.session.get(captcha_url, headers=self.headers)
        with open('cptcha.gif', 'wb') as f:
            f.write(response.content)
        # write the captcha into a local file
        print('Sorry but you might need to input the captcha manually. It is in the same directory as login.py.')
        captcha = input('Captcha:')
        return captcha

if __name__ == '__main__':
    Login().main()