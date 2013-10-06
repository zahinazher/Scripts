#**************************************
# The script requires 1 input files <credentials.csv> <sender_username>
# You can give any name to these files. 
# The id.csv file contains facebooks ids in the first column
# The credentials.csv file contains sender email in its first column and 
# corresponding password in its 2nd column

# Alert!
# Some class functions have deliberately been omitted due to copyright reasons. Hence do not try to use this code.



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
#from crawler import *
import selenium
from BeautifulSoup import BeautifulSoup
from selenium import webdriver


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
			username_list = []
			for row in file2_reader:
				email_list.append(row[0])
				password_list.append(row[1])
				username_list.append(row[2])
                       	return (email_list,password_list,username_list)


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


	def get_sender_user_name(self,response):

		#f= open('resp.txt' , 'w')
		#soup = BeautifulSoup(response)
		#f.write(str(response))
		data = response.find('body')

		if re.search(r'"name".*?"firstName":".*?","vanity":".*?"',str(data),re.I):
			sender_username = re.search(r'"name".*?"firstName":".*?","vanity":".*?"',str(data),re.I).group()
			sender_username = re.sub(r'"','',re.sub(r'.*?"vanity":"','',sender_username,re.I))
			#print sender_username
			return sender_username
		else:
			return 'NA'

	def main(self):

		(email_list,password_list,sender_username) = self.get_email_pass()
		
		#print lsd,default_persistent,lgnrnd,locale,cookie_datr
		self.email = email_list[self.count_senders]
		self.password = password_list[self.count_senders]
		self.username = sender_username[self.count_senders]

		driver = webdriver.Firefox()
		driver.get(self.url)
		ele1 = driver.find_element_by_name("email")
		ele1.clear()
		ele1.send_keys(self.email)
		ele2 = driver.find_element_by_name("pass")
		ele2.clear()	
		ele2.send_keys(self.password)
		self.count1 = 0
		self.check1 = True
		variables=['u','e','c','l','a','b','v','d','x','z','f']
		while self.check1 != False:
			val = variables[self.count1]
			value = 'u_0_'
			value = value + str(val)
			print value
			try: 
				ele3 = driver.find_element_by_id(value)
				ele3.click()
				self.check1 = False

			except Exception as e:
				#print "exx: "+str(e)
				self.check1 = True
			except:
				self.check1 = True
				pass

			self.count1+=1

		#ele4 = driver.find_elements_by_class_name("navLink bigPadding")
		#ele4[2].click()
		
		#driver.get(self.url)
		#assert "Messages" in driver.page_source
		#resp = driver.page_source.encode('ascii', 'ignore')

		#resp = BeautifulSoup(resp)
		#sender_username = self.get_sender_user_name(resp)
		#print sender_username

		url8 = 'https://www.facebook.com/' + str(self.username) + '/friends_all'
		driver.get(url8)
		
		#time.sleep(6)
		assert "All Friends" in driver.page_source 
		time.sleep(6)

		self.count3 = 0
		#while "More About" not in driver.page_source:
		while "Watched" not in driver.page_source:
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			print self.count3
			self.count3 += 1


		soup = BeautifulSoup(driver.page_source)
		result= soup.findAll('div',attrs={'class':'fsl fwb fcb'})
		result= soup.findAll('a')
		#print result
		array_id = []
		for link in result:
                	line=link.get('data-hovercard')
			if line == None:
				pass
			else:
				if re.search(r'\?id=.*?&',str(line),re.I):
					line = re.search(r'\?id=.*?&',str(line),re.I).group()
					line = re.sub(r'&','',re.sub(r'\?id=','',str(line),re.I))
					array_id.append(line)
		#print array_id
		sorted_array_id = sorted(array_id)
		#print sorted_array_id
	
		index=0 ; # index of each row
		count_unique=0 ; 
		check = False # if consecutive md5sum are uneqaul
    
		f = open('all_friends_id.txt' , 'w')
		for arr in sorted_array_id:
		    if index < len(sorted_array_id):
			if index == len(sorted_array_id)-1:
			    next_md5sum = "junkvalue"
			    #print row
			else:
			    next_md5sum = sorted_array_id[index+1]
			if sorted_array_id[index] == next_md5sum:
			    check=True
			else:
			    check=False
			if (check==False): # if unique md5sum 
			    count_unique+=1
			    f.write(arr+'\n')
		    index+=1



		"""for a_ref in array_href:
			if re.search(r'\?id=.*?&',str(a_ref),re.I):
				a_ref = re.search(r'\?id=.*?&',str(a_ref),re.I).group()
				a_ref = re.sub(r'&','',re.sub(r'\?id=','',str(a_ref),re.I))
				print a_ref"""

		#f=open('resp3', 'w')
		#f.write(str(soup))
		#driver.close()


if __name__ == '__main__':
	if len(sys.argv)!=2 :
		print "     Incorrect input paramaters    "
		print "*********How to run the script*****"
		print "python test1.py <credentials.csv> <sender_username>"
		sys.exit(1)
	fbook = book()
	fbook.main()
