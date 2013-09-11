import sys
import os
import csv
import optparse
import hashlib
import urllib2
import urllib
import urlparse
import MultipartPostHandler
import cookielib
import re
import time
import json
from BeautifulSoup import BeautifulSoup
import socket

class norton:
    
	def __init__(self, input):
		self.input = input
		URL  = 'http://safeweb.norton.com/report/show?url=memothis.co.kr'
		self.__url = URL 
		self.__opt = {'Email Address':'zahin@ebryx.com',  'Password' :'budd00009'}
		headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'User-Agent' : 'Mozilla/5.0(compatible; MSIE 9.0; Windows NT 6.1; Trident/ 5.0; BOIE;ENUSMSNIP)',
                'Accept-Encoding': 'deflate',
                'Connection': 'keep-alive',
                'Referer': 'https://safeweb.norton.com',
                'Accept-Language' : 'en-us,en;q=0.5', 
                'Content-Type':	'application/x-www-form-urlencoded'}
                self.__headers = headers
    
	def Isnetworkon(self):
		try:
			response=urllib2.urlopen('http://www.google.com', timeout=5)
			return True
		except urllib2.URLError as err: 
			print "except error"
			pass
			return False
		except socket.timeout:
			self.Isnetworkon()
    
	def getNorton(self):
        	try:
			op=open('opfile.txt',"w")
			op1=open('opfile1.txt',"w")
		except IOError:
			print "Error opening text File", op
			sys.exit()

		check_flag=1
		while(check_flag == 1):
			if(self.Isnetworkon() == True):
				check_flag = 0
				data = urllib.urlencode(self.__opt)
				request = urllib2.Request(self.__url, data, self.__headers)
				response = urllib2.urlopen(self.__url)
				#print "request",request
				cookies = cookielib.CookieJar()
				try:
					cookies.extract_cookies(response,request)
				except:
					print"no response"
				#print "cookies",cookies
				cookie_handler= urllib2.HTTPCookieProcessor( cookies )
				redirect_handler= urllib2.HTTPRedirectHandler()
				opener = urllib2.build_opener(redirect_handler,cookie_handler)
				#print "opener",opener
				resp_open = opener.open(self.__url)
				resp=resp_open.read()
				op.write(resp)
				print resp
				summary=re.search(r'<div id="header-menu-bar>.*?</h1>',resp)
				print summary
				if summary:
					summary=summary.group(0)
					#op1.write(summary)
					print"summary",summary
				else:
					print "summary = empty"
									

			else:
				pass

if __name__ == '__main__':
	nort = norton('http://www.google.com')
	nort.getNorton()
	 
