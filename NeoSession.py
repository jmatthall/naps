#!/usr/bin/env python3
'''Neopets login.'''

import requests
import pickle
import json
import os
import sys
import random
import time
import configparser as cp


class NeoSession:
    '''Login to neopets.com'''
    conf = cp.ConfigParser()
    conf.read('settings.conf')
    session = requests.Session()
    username = conf['USER-SETTINGS']['USERNAME']
    login_data = {'username': username,
                  'password': conf['USER-SETTINGS']['PASSWORD'], }
    jar = conf['PROGRAM-SETTINGS']['COOKIE_JAR']
    #pause = time.sleep(random.randint(5, 11))

    def __init__(self):
        self.load_session_cookies()
        self.load_session_headers()
        self.login()
        self.update_session_cookies()

    def session_get(self, url):
        time.sleep(random.randint(5, 11))
        return self.session.get(url)
        self.session.headers.update({'Referer': url})

    def session_post(self, url, data=None):
        time.sleep(random.randint(5, 11))
        if data is None:
            return self.session.post(url)
        else:
            return self.session.post(url, data)
        self.session.headers.update({'Referer': url})

    def update_session_cookies(self):
        if os.path.isfile(self.jar):
            with open(self.jar, 'wb') as jar:
                pickle.dump(self.session.cookies, jar)

    def load_session_cookies(self):
        if os.path.isfile(self.jar):
            with open(self.jar, 'rb') as jar:
                session_cookies = pickle.load(jar)
                self.session.cookies.update(session_cookies)

    def load_session_headers(self):
        with open(self.conf['PROGRAM-SETTINGS']['HEADERS'], 'r') as headers:
            session_headers = json.load(headers)
            self.session.headers.update(session_headers)

    def check_login(self):
        url = 'http://www.neopets.com/'
        resp = self.session_get(url)
        if 'Welcome, <a href="/userlookup.phtml?user={}">'.format(
                self.username) in resp.text:
            print('Already logged in.')
            return True

    def login(self):
        '''Log-in to neopets.com'''
        if self.check_login() is not True:
            url = 'http://www.neopets.com/login'
            resp = self.session_get(url)
            self.session.headers.update({'Referer': url})

            try:
                resp.raise_for_status()
            except requests.exceptions.HTTPError:
                print('Could not connect to neopets.com')
                sys.exit(1)

            if os.path.isfile(self.jar) is not True:
                os.system('touch neopets.cookies')
                self.session_cookies = resp.cookies
                return self.session_cookies
            url = 'http://www.neopets.com/login.phtml'
            self.session_post(url, self.login_data)
            print('Login successful.')


def main():
    NeoSession()


if __name__ == '__main__':
    main()