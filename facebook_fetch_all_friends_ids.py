#**************************************
# The script requires 1 input files <credentials.csv>
# You can give any name to these files. 
# The id.csv file contains facebooks ids in the first column
# The credentials.csv file contains sender email in its first column and 
# corresponding password in its 2nd column

# Alert!
# Some class functions have deliberately been omitted due to copyrights reasons. Hence do not try to use this code.

import re
import os
import csv
import sys
import urllib
import urllib2
import cookielib
import time
import datetime
import logging
import json
import socket
from ghost import Ghost
from crawler import *
from BeautifulSoup import BeautifulSoup

#urllib2.HTTPRedirectHndler()
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj),urllib2.HTTPSHandler())
urllib2.install_opener(opener) # globally it can be used with urlopen

class book:
	# Declare Static Variables 
	mesg_per_sender = 10
	mesg_count_for_sleep = 30
	count_recepients = 0
	count_senders = 0
	check = True # check for messages per user

	url = 'https://www.facebook.com'
	url1 = 'https://www.facebook.com/login.php?login_attempt=1'
	url2 = 'https://www.facebook.com/logout.php'
	url4 = 'https://www.facebook.com/settings'
	url5 = 'https://www.facebook.com/ajax/add_friend/action.php'
	url7 = 'https://www.facebook.com/ajax/bz'


	def __init__(self):
		print "Initializing..."
		now = datetime.datetime.now()
		logging.basicConfig(filename='logs.log')
		logging.critical('Date: '+str(now))

	def get_email_pass(self):
		with open(sys.argv[1], 'rb') as f:
			try:
				file2_reader = csv.reader(f, delimiter=',')
			except IOError:
				print "Error Reading csv File", f
				sys.exit()
			email_list = []
			password_list = []
			for row in file2_reader:
				email_list.append(row[0])
				password_list.append(row[1])
                       	return (email_list,password_list)


	def get_cookie(self):
		try:
			for cookie in cj:
				if cookie.name == 'datr':
		      			cookie_datr = cookie.value
				if cookie.name == 'reg_fb_gate':
		      			cookie_reg_fb_gate = cookie.value
				if cookie.name == 'reg_fb_ref':
		      			cookie_reg_fb_ref = cookie.value
				return cookie_datr
		except:
			return 'NA'


	def get_response(self,URL,data):
		try:
			request = urllib2.Request(URL,data)
			response = urllib2.urlopen(request)
			return response
		except urllib2.HTTPError as e:
			#print "HTTP error" , e.code
			logging.warning('HTTP error:' + str(e.code))
			#pass
		except urllib2.URLError as e1:
			#print "urllib.URLError",e1
			logging.warning('URLError:' + str(e1))
			#pass
			"""while (self.check_connectivity() == False):
				pass"""
		except Exception as e:
			print "Exception:",e
			logging.warning(str(e))

	def get_post_data(self,response):
		#print response.read()
		try:
			soup = BeautifulSoup(response)
			lsd = soup.find('input', type='hidden', attrs={'name': 'lsd'})
			lsd = lsd['value']
			lsd = str(lsd)

			default_persistent = soup.find('input', type='hidden', attrs={'name': 'default_persistent'})
			default_persistent = default_persistent['value']
			default_persistent = str(default_persistent)

			"""timezone = soup.find('input', type='hidden', attrs={'name': 'timezone'})
			timezone = timezone['value']
			timezone = str(timezone)"""

			lgnrnd = soup.find('input', type='hidden', attrs={'name': 'lgnrnd'})
			lgnrnd = lgnrnd['value']
			lgnrnd = str(lgnrnd)

			"""lgnjs = soup.find('input', type='hidden', attrs={'name': 'lgnjs'})
			lgnjs = lgnjs['value']
			lgnjs = str(lgnjs)

			lgnjs = soup.find('body')
			if (re.search(r'tz_calculate.*',str(lgnjs))):
				lgnjs = re.search(r'tz_calculate.*',str(lgnjs)).group()
				lgnjs = re.search(r'\(.*?\)',str(lgnjs)).group()
				lgnjs = re.sub(r'\(','',re.sub(r'\)','',lgnjs,re.M|re.I))
				lgnjs = str(lgnjs)"""

			locale = soup.find('input', type='hidden', attrs={'name': 'locale'})
			locale = locale['value']
			locale = str(locale)

			return (lsd,default_persistent,lgnrnd,locale)
		except Exception as e:
			#print "get_post_data:",e
			logging.warning(str(e))
			#pass

	def get_message_post_data1(self,response):

		#data = BeautifulSoup(response)
		data = response.find('head')
		
		fb_dtsg = response.find('input', type='hidden', attrs={'name': 'fb_dtsg'})
		fb_dtsg = fb_dtsg['value']
		fb_dtsg = str(fb_dtsg)

		if re.search(r'\({"user":".*?"',str(data),re.I):
			sender_fbid = re.search(r'\({"user":".*?"',str(data),re.I).group()
			sender_fbid = re.sub(r'"','',re.sub(r'\({"user":"','',sender_fbid,re.I))
		else:
			sender_fbid = 'NA'

		if re.search(r'"ajaxpipe_token":".*?"',str(data),re.I):
			ajaxpipe_token = re.search(r'"ajaxpipe_token":".*?"',str(data),re.I).group()
			ajaxpipe_token = re.sub(r'"','',re.sub(r'"ajaxpipe_token":"','',ajaxpipe_token,re.I))
		else:
			ajaxpipe_token = 'NA'


		return (sender_fbid,fb_dtsg,ajaxpipe_token)

	def get_message_post_data2(self,response):

		data = response.find('body')
		if re.search(r'"uid":.*?}',str(data),re.I):
			receiver_fbid = re.search(r'"uid":.*?}',str(data),re.I).group()
			receiver_fbid = re.sub(r'}','',re.sub(r'"uid":','',receiver_fbid,re.I))
		else:
			receiver_fbid = 'NA'
		return receiver_fbid

	def get_sender_user_name(self,response):

		data = response.find('body')

		if re.search(r'section=username.*?</strong>',str(data),re.I):
			sender_username = re.search(r'section=username.*?</strong>',str(data),re.I).group()
			sender_username = re.search(r'<strong>.*?</strong>',str(sender_username),re.I).group()
			sender_username = re.sub(r'<strong>','',re.sub(r'</strong>','',sender_username,re.I))
			#print sender_username
			return sender_username
		else:
			return 'NA'

	def get_friends_ids(self,response):

		data = response.find('body')
		data_a = data.findAll('a')
		print data_a
		
	def main(self):

		(email_list,password_list) = self.get_email_pass()
		
		#print lsd,default_persistent,lgnrnd,locale,cookie_datr
		self.email = email_list[self.count_senders]
		self.password = password_list[self.count_senders]
		try:
			cj.clear()
			request = urllib2.Request(self.url)
			response = urllib2.urlopen(request)
			(lsd,default_persistent,lgnrnd,locale) = self.get_post_data(response)
			cookie_datr = self.get_cookie()
			
		except:
			logging.warning('no network connectivity')
			pass

		try:
			details={ 'lsd' : lsd , 'email' : self.email ,
				 'pass' : self.password , 
				 'default_persistent': default_persistent ,
				 'timezone' : '' , 'lgnrnd' : lgnrnd ,
				 'lgnjs' : '' , 'locale' : locale}

			data = urllib.urlencode(details)
			response = self.get_response(self.url1,data)  # send login request

			response = self.get_response(self.url,None)
			response = BeautifulSoup(response)
			(sender_fbid,fb_dtsg,ajaxpipe_token) = self.get_message_post_data1(response)
			#print sender_fbid,fb_dtsg, ajaxpipe_token

			try:
				resp = str(response)
				if "Update Status"  in resp:
					print "logged in successfully as : ",self.email
				else:
					print "Login failed"

			except Exception as e:
				print logging.warning('login failed exception: ' + str(e))

			response = self.get_response(self.url4,None)
			response = BeautifulSoup(response)
			(sender_username) = self.get_sender_user_name(response)

		except:

			logging.warning('login failed:' + email_list[self.count_senders])
				
		#try: 

		url6 = 'https://www.facebook.com/' + sender_username + '/friends_all'
		#url6 = 'https://www.facebook.com/ajax/friends/status.php'
		#url6 = 'https://www.facebook.com/ajax/friends/lists/flyout_log.php'

		ghost = Ghost()

		"""response = self.get_response(url6,None)

		response = BeautifulSoup(response)
		f = open('resp.txt' , 'w')
		f.write(str(response))"""


		"""url8 = 'https://www.facebook.com/' + sender_username + '/friends?' + \
			'__user=' + sender_fbid + \
			'&__a=1' + \
			'&__req=jsonp_4&__adt=4'
			#'ajaxpipe=1&ajaxpipe_token='+ ajaxpipe_token + \
			#'&quickling[version]=950967%3B0%3B1%3B0%3B' + \

		print url8"""

		cmd = os.popen("python crawler.py -u " +  url6 + " -f " + 'mbl.txt') 
		cmd.close()

		file1 = open('mbl.txt','r')
		response  = file1.readlines()
		response = response[0]
		soup = BeautifulSoup(response)

		#f = open('fetch_id1.txt' , 'w')
		#f.write(str(soup))

		#except:
			#logging.warning('Fetching all friends ids failed' )


		print "Execution Complete"

if __name__ == '__main__':
	if len(sys.argv)!=2 :
		print "     Incorrect input paramaters    "
		print "*********How to run the script*****"
		print "python test1.py <credentials.csv>"
		sys.exit(1)
	fbook = book()
	fbook.main()

