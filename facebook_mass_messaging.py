#**************************************
# The script requires 3 input files id.csv, <message.txt credentials.csv message_per_sender
# You can give any name to these files. 
# The id.csv file contains facebooks ids in the first column
# The credentials.csv file contains sender email in its first column and 
# corresponding password in its 2nd column
# The message.txt file contains the message to be sent


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
	check = True
	url = 'https://www.facebook.com'
	url1 = 'https://www.facebook.com/login.php?login_attempt=1'
	url2 = 'https://www.facebook.com/logout.php'
	url4 = 'https://www.facebook.com/ajax/mercury/send_messages.php'

	def __init__(self):
		print "Initializing..."
		now = datetime.datetime.now()
		logging.basicConfig(filename='logs.log')
		logging.critical('Date: '+str(now))

	def get_ids(self):
		with open(sys.argv[1], 'rb') as f:
			try:
				file2_reader = csv.reader(f, delimiter=',')
			except IOError:
				print "Error Reading csv File", f
				sys.exit()
			ids = []
			for row in file2_reader:
				ids.append(row[0])
                       	return (ids)

	def get_email_pass(self):
		with open(sys.argv[3], 'rb') as f:
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

	def get_message(self):
		try:
			mesg =open(sys.argv[2],"r+")
		except IOError:
			print "Error Reading text File", mesg
			sys.exit()

		mesg = mesg.read()
		return mesg

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
		return (sender_fbid,fb_dtsg)

	def get_message_post_data2(self,response):
		data = response.find('body')
		if re.search(r'"uid":.*?}',str(data),re.I):
			receiver_fbid = re.search(r'"uid":.*?}',str(data),re.I).group()
			receiver_fbid = re.sub(r'}','',re.sub(r'"uid":','',receiver_fbid,re.I))
		else:
			receiver_fbid = 'NA'
		return receiver_fbid

	def main(self):
		id_list = self.get_ids()
		message = str(self.get_message())
		(email_list,password_list) = self.get_email_pass()
		
		#print lsd,default_persistent,lgnrnd,locale,cookie_datr
		
		for recepient_id in id_list:
			self.count_recepients += 1 

			if (self.count_recepients%self.mesg_count_for_sleep) == 0:
				time.sleep(2)  # sleep call after sending several messsages

			if self.check == True: # if its time to use a new sender
				#print "enter new email",email_list[self.count_senders]
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


				details={ 'lsd' : lsd , 'email' : self.email , 'pass' : self.password , 'default_persistent': default_persistent , 'timezone' : '' , 'lgnrnd' : lgnrnd , 'lgnjs' : '' , 'locale' : locale}
				data = urllib.urlencode(details)

				try:
					response = self.get_response(self.url1,data)  # send login request

					response = self.get_response(self.url,None)
					response = BeautifulSoup(response)
					(sender_fbid,fb_dtsg) = self.get_message_post_data1(response)
					#print sender_fbid,fb_dtsg

					"""try:
						resp = str(response)
						if "Update Status"  in resp:
							print "logged in successfully as : ",self.email
						else:
							print "Login failed"
					except Exception as e:
						print "Login failed Exception:",e"""
				except:
					self.count_senders +=1
					self.check = True
					logging.warning('login failed:' + self.email)
					
			print 'message',self.count_recepients
			#logging.warning('message:'+str(self.count_recepients))
			url3 = 'https://www.facebook.com/' + str(recepient_id)
			response = self.get_response(url3,None) # receiver's home page 
			try:
				resp = BeautifulSoup(response)
				receiver_fbid = self.get_message_post_data2(resp)
				#print receiver_fbid

				send_fbid = 'fbid:'+str(sender_fbid)
				rece_fbid = 'fbid:'+str(receiver_fbid)
				#      message_batch[0][force_sms]	true // b4 push phase
				details={'message_batch[0][action_type]' : 'ma-type:user-generated-message',
				'message_batch[0][thread_id]': '',
				'message_batch[0][author]': send_fbid,
				'message_batch[0][author_email]':'',
				'message_batch[0][coordinates]':'',
				'message_batch[0][timestamp]':'',
				'message_batch[0][timestamp_absolute]':'Today',
				'message_batch[0][timestamp_relative]':'',
				'message_batch[0][timestamp_time_passed]':'0',
				'message_batch[0][is_unread]':'false',
				'message_batch[0][is_cleared]':'false',
				'message_batch[0][is_forward]':'false',
				'message_batch[0][is_filtered_content]':'false',
				'message_batch[0][is_spoof_warning]':'false',
				'message_batch[0][source]':'source:chat:web',
				'message_batch[0][source_tags][0]':'source:chat',
				'message_batch[0][body]': message,
				'message_batch[0][has_attachment]':'false',
				'message_batch[0][html_body]':'false',
				'message_batch[0][specific_to_list][0]':rece_fbid,
				'message_batch[0][specific_to_list][1]':send_fbid,
				'message_batch[0][ui_push_phase]':'V3',
				'message_batch[0][status]':'0',
				'message_batch[0][message_id]':'',
				'client':'mercury',
				'__user':str(sender_fbid),
				'__a':'1',
				'__dyn':'',
				'__req':'',
				'fb_dtsg':fb_dtsg,
				'ttstamp':''}
				data = urllib.urlencode(details)
				response = self.get_response(self.url4,data) # send message to recepient
				request.add_header('Cookie', cookie_datr)
				resp = BeautifulSoup(response)

				if len(email_list) != 1:
					if (self.count_recepients%self.mesg_per_sender) == 0: # sender is changed after every ? messages
						self.check=True
						self.count_senders+=1
					else:
						self.check = False

					if self.count_senders == (len(email_list)):# if all senders are used, restart count 
						self.count_senders = 0
						self.check = True
				else:
					self.check == False

			except Exception as e:
				logging.warning('recepient incorrect id:' + str(recepient_id))
				pass
		print "Execution Complete"

if __name__ == '__main__':
	if len(sys.argv)!=4 :
		print "     Incorrect input paramaters    "
		print "*********How to run the script*****"
		print "python test1.py <id.csv> <message.txt> <credentials.csv>"
		sys.exit(1)
	fbook = book()
	fbook.main()

	
