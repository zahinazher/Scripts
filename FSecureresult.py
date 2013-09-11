import urllib2
import urllib
import urlparse
import MultipartPostHandler
import cookielib
import sys
import os
import csv
import optparse
import hashlib
import re
import time
from BeautifulSoup import BeautifulSoup
import socket

class FSecure:
    
	def __init__(self, input):
		self.input = input
		URL  = 'http://browsingprotection.f-secure.com/'
		self.__url = URL 
		headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'User-Agent' : 'Mozilla/5.0(compatible; MSIE 9.0; Windows NT 6.1; Trident/ 5.0; BOIE;ENUSMSNIP)',
                'Accept-Encoding': 'deflate',
                'Connection': 'keep-alive',
                'Referer': 'https://safeweb.norton.com/report/',
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
    
	def getFsecure(self):
        
		try:
			check_flag = 1
			html = ''	
			while(check_flag == 1):
				if(self.Isnetworkon() == True):
					check_flag = 0
					cj = cookielib.CookieJar()
					opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
					home = opener.open('http://browsingprotection.f-secure.com/swp/')
					sessid = cj._cookies['browsingprotection.f-secure.com']['/swp']['JSESSIONID'].value
					self.__headers['Cookie'] = 'JSESSION=' + sessid
					html = home.read()
					ls = re.findall(r'(action=";.*?>)', str(html))  
					id = ls[1]
					id = id.split('=')
					id = id[3]
					id = re.sub(r'">','',id)
					URL = self.__url + 'swp/?x=' + id
					raw_params = {}
					raw_params['url'] = self.input
					raw_params['boxstate'] = '1'
					params = urllib.urlencode(raw_params)
					request = urllib2.Request(URL, params, self.__headers)
					response = urllib2.urlopen(request)
					html = response.read()
					soup = BeautifulSoup(''.join(html))
				else:
					check_flag = 1
                
				
				if re.search(r'("error_message_id">.*?</span>)', str(soup)):
					return 'invalid site'
				else:
                    
					font = soup.findAll('font')
					font = font[0]
					res = re.search(r'<b>.*?</b>', str(font)).group()
					res = re.sub(r'<b>','',re.sub(r'</b>','',res))
					return res
		except:
			pass


