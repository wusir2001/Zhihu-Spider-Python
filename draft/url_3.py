# !/usr/bin/env python
# -*- coding: utf-8 -*-


import ConfigParser
import requests
from time import time
from bs4 import BeautifulSoup
import sys
import math

reload(sys)
sys.setdefaultencoding('utf-8')



# read the email and password recorded in the file 'config.ini'
config = ConfigParser.ConfigParser()
config.read('config.ini')
email = config.get('info', 'email')
password = config.get('info', 'password')

# create an instance of requests(module)
session = requests.session()


class ZhihuLogin(object):
    '''
    Login in www.zhihu.com firstly

    '''
    def __init__(self):
	'''
	define some essential objects, and get cookies for login in Zhihu.
	param str email
	param str password
	param dic header
	'_xsrf': an random value, essential part of the form data for login. included in the cookies, or could be accessed from the web page.
	'''
        self.login_url = 'http://www.zhihu.com/login'
	self.email = email
        self.password = password
	s = session.post(self.login_url)
        self._xsrf = dict(s.cookies)['_xsrf']
        self.header = {
		    'X-Requested-With': 'XMLHttpRequest',
                    'Connection': 'Keep-Alive',
                    'Accept': 'text/html, application/xhtml+xml, */*',
                    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
                    'Accept-Encoding': 'gzip, deflate',
                    'Host': 'www.zhihu.com',
                    'DNT': '1'
                    }
        self.data = {'email': email,
                    'password': password,
                    '_xsrf': self._xsrf,  # get from the cookies
                    'rememberme': 'y'}



    def captcha(self):
	'''
	Download the figure for captcha.
	'''
        captcha_url = 'http://www.zhihu.com/captcha.gif?r=' + str(int(time()*1000))
        captcha = session.get(captcha_url)
        with open('captcha.gif', 'wb') as f:
            f.write(captcha.content)



    def login(self):
	'''
	Post the data for login.
	'''
        response = session.post(self.login_url, data = self.data, headers = self.header)
        return response



    def main(self):
	'''
	post the data and login in, return the result of this trival.
	'''
	session.headers.update(self.header)
	response = self.login()  # May fail due to the captcha. If so, login in after processing the captcha.       
	# judge if login successfully
        json = response.json()
	code = json['r']
        if code == 0:
            print 'Login Successfully !!!'
        elif code == 1:  # It's most likely that there is the captcha.
            self.captcha()
            print 'We have to input the captcha.\nPlease open the file captcha.gif.\n'
            captcha = raw_input('Enter the characters on the figure here: ')
            captcha = str(captcha)
            self.data['captcha'] = captcha  # Add the values of the captcha in the form data.
            response = self.login()  # Try to login in again.
            json = response.json()
            code = json['r']  # Check if login in successfully the second time.
            if code == 1:
                print 'Login Failed !!!'
                for code, description in json.items():
                    print 'Here is the information about the failure login, %s: %s' %(code, description)
            elif code == 0:
                print 'Login Successfully!'
            else:
                print 'OOPS! Please dno\'t to hesitate with me, and I will fix this error asap.'
	else:
	    print 'OOPS! Please dno\'t to hesitate with me, and I will fix this error asap.'

ZhihuLogin().main()

url_initial_page = 'http://www.zhihu.com/'
url_topic = 'http://www.zhihu.com/topics'
url_follower = 'http://www.zhihu.com/question/29873359/followers'
url_topic = 'http://www.zhihu.com/topic/19767666'
url_question = 'http://www.zhihu.com/question/29755376'
url_people = 'http://www.zhihu.com/people/7sdream'
url_many_answer = 'http://www.zhihu.com/question/29762631'


s = session.post(url_follower)
_xsrf = dict(s.cookies)['_xsrf']


ZhihuLogin.header['referer'] = url_follower


response = session.get(url_follower)
soup = BeautifulSoup(response.content)

print soup.title


# pattern = re.compile('<div.*?class="topic-feed-item".*?a.*?href="(.*?)"')


# peoples = soup.find_all('div', class_ = 'topic-feed-item')
# print 'length of peoples', len(peoples)
# print 'type of peoples: ', type(peoples)
# for people in peoples:
#     print people
#    print 'type of people: ',type(people)





