# -*- coding: 'utf-8' -*-
# http://www.bilibili.com/video/av11541930/

import requests
import getpass
from html.parser import HTMLParser
from PIL import Image

class DoubanClient(object):
	"""docstring for DoubanClient"""
	def __init__(self):
		self.headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'}
		self.session = requests.session()

	def login(self,username,password, #登陆的函数
		      source = 'index_nav',
		      redir = 'https://www.douban.com/',
		      login = '登陆'):
		login_url = 'https://accounts.douban.com/login'

		response = self.session.get(login_url)
		(captcha_id,captcha_url) = _get_captcha(response.content) #获取验证码的id和url
		print(captcha_id)

		if captcha_id:
			r = self.session.get(captcha_url)
			with open('captcha.jpg','wb') as f:
				f.write(r.content)

			try:
				im = Image.open('captcha.jpg')
				im.show()
				im.close()
			except:
				print (u'请输入验证码')

			captcha_solution = input('please input solution for captcha [{}]'.format(captcha_url))

		data = {'form_email':username,
		        'form_password':password,
		        'source':source,
		        'redir':redir,
		        'login':login}
		if captcha_id:
			data['captcha-id'] = captcha_id
			data['captcha-solution'] = captcha_solution

		self.session.post(login_url,data=data,headers=self.headers) #登陆的请求

		print(self.session.get('https://www.douban.com').content)  #访问主页


def _attr(attrs,attrname):
	for attr in attrs:
		if attr[0] == attrname:
			return attr[1]
	return None



def _get_captcha(content):

	class CaptchaParse(HTMLParser):  # 解析网页的类
		def __init__(self):
			HTMLParser.__init__(self) # 初始化
			self.captcha_id = None
			self.captcha_url = None

		def handle_starttag(self,tag,attrs):  # 标签 属性 name id class
			if tag == 'img' and _attr(attrs,'id') == 'captcha_image' and _attr(attrs,'class') == 'captcha_image':	
				self.captcha_url = _attr(attrs,'src')

			if tag == 'input' and _attr(attrs,'type') == 'hidden' and _attr(attrs,'name') == 'captcha-id':
				self.captcha_id = _attr(attrs,'value')

	p = CaptchaParse() # 实例这个类
	p.feed(content.decode('UTF-8'))  # 把需要解析的数据传到feed方法
	return p.captcha_id,p.captcha_url   # 把匹配到的数据返回 


if __name__ == '__main__':
	username = input('please input your username:')
	password = getpass.getpass('please input your password:')
	D = DoubanClient()
	D.login(username,password)