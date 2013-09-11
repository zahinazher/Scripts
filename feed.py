#####################################################################
#                   How to run the Script
#
#Terminal takes filename as the only command line input
#
#- terminal command input
#	$ python <path to code> <path to csv file> 
#	e.g python feed.py filename.csv
#####################################################################
import urllib2
import urllib
import cookielib
import sys
import os
from BeautifulSoup import BeautifulSoup
import re
import string
import csv
import threading
import math
################# Please Enter the Required Data ######################
username = ''
password = ''
twittername = ''
NumberOfThreads= 4
proxy = urllib2.ProxyHandler({'https':'https://127.0.0.1:8008'})
############################ Thank You #################################

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPRedirectHandler(),urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener) # globally it can be used with urlopen

class rss_feeds:
	def readfile(self,filename):
		with open(filename, 'rb') as f:
		    reader = csv.reader(f)
		    feednames = []
		    feedurls = []
		    try:
			for row in reader:
			    feednames.append(row[0])
			    feedurls.append(row[1])
			return (feednames,feedurls)
		    except csv.Error, e:
			sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))
		f.close()


	def get_auth_token(self,response):
		soup = BeautifulSoup(response)
		auth_token = soup.find('input', type='hidden', attrs={'name': 'authenticity_token'})
		authtoken = auth_token['value']
		authtoken = str(authtoken)
		return authtoken

	def get_cookie(self,info):
		if 'set-cookie' in info:
		  	cookie = info['set-cookie']
			cookie = cookie[:string.find(cookie, ';')]
			#print "cookie is present "
		else:
			print "no cookie"

	def get_response(self,URL,data):
		try:
			#response= opener.open(URL, data)
			request = urllib2.Request(URL, data)
			response = urllib2.urlopen(request)
		except urllib2.HTTPError as e:
			print "HTTP error" , e.code		
		return response


	def feed_configure(self,authtoken,i1, i2):
		rangecheck=True
		if range(i1,i2)==[]:
			rangecheck=False
		if rangecheck==True:
			for i in range(i1,i2):
				rssfeed= {'t_feed':feedurls[i],'authenticity_token': authtoken, '_':''}
				data = urllib.urlencode(rssfeed)

				URL3='http://twitterfeed.com/feed/feedtest'
				#response = self.get_response(URL3,data)
				request = urllib2.Request(URL3, data)
				response = urllib2.urlopen(request)
				#print response.geturl()
				resread=response.read()
				check= True
				if "Feed parsed" in resread:
					check=True
					#print "Feed Passed"
				else:
					#print "Feed not Passed"
					check=False
					continue

				if check==True:
					rssfeed= {'authenticity_token': authtoken,'feed[feedname]':feednames[i],
					'feed[feedurl]':feedurls[i],
					'feed[isactive]':'0','feed[isactive]':'1','feed[freq_id]':'7','feed[limit_id]':'1','feed[showdesc]':'1',
					'feed[showurl]':'0','feed[showurl]':'1','feed[shortener_id]':'4','feed[shortpartner]':'','feed[shortpartner2]':'',
					'feed[li_image_url]':'','feed[checkmethod_id]':'1','feed[guid_sorted]':'0','feed[guid_sorted]':'1',
					'feed[prestring]':'','feed[poststring]':'','feed[keywords]':''}
					data = urllib.urlencode(rssfeed)
					URL4='http://twitterfeed.com/feeds'
					#response=self.get_response(URL4,data)
					request = urllib2.Request(URL4, data)
					response = urllib2.urlopen(request)
					finalUrl=response.geturl()
					#print finalUrl
					resread=response.read()
					if "successfully created" in resread:
						#print "Feed was successfully created"
						pass
					else :
						print "Feed not created because there were no publish dates or GUIDs"
						continue

					host = re.search(r'http://twitter.*?/feeds/.*?/',finalUrl, re.I)
					if host:
						host = host.group()
					else:
						continue
					URL5 = host + 'services'
					rssfeed= {'authenticity_token': authtoken,'service[posttype_id]':'1',
						'service[params][twittername]':twittername,
						'service[utm_source]':'twitterfeed',
						'service[utm_medium]':'twitter',
						'service[utm_campaign]':'',
						'service[utm_term]':'',
						'service[utm_content]':''}
					data = urllib.urlencode(rssfeed)
					#response=self.get_response(URL5,data)
					request = urllib2.Request(URL5, data)
					response = urllib2.urlopen(request)
					finalUrl=response.geturl()
					#print finalUrl
					resread=response.read()
					if "Service created successfully" in resread:
						#print "Service created successfully"
						pass
					else :
						#print "Service was not created"
						pass

					URL6 = host + 'confirm'
					#print "URL6 : ", URL6
					response = urllib2.urlopen(URL6)
					resread= response.read()
					if "successfully configured" in resread:
						print "Feed configured", feedurls[i]
					else :
						print "Feed not configured properly", feedurls[i]

					print "Success"
				else:
					print "Failure"


	def main(self):
		#os.environ['http_proxy'] = "http://10.8.0.1:8118/"  # does not work with urllib2

		if len(sys.argv) !2:
			print "*****INcorrect input parameters****
			print "Usage: python <path to code> <path to csv file> 
			sys.exit()
		else:
			filename=sys.argv[1]
			(feednames,feedurls) = self.readfile(filename)
			URL = 'http://www.twitterfeed.com'
			#response= opener.open(URL)
			request = urllib2.Request(URL)
			response = urllib2.urlopen(request)

			authtoken=self.get_auth_token(response)
			info=response.info()
			cookie=get_cookie(info)

			details={'email' : username, 'password' : password, 'authenticity_token': authtoken}
			data = urllib.urlencode(details)
			URL2 = 'http://twitterfeed.com/session'
			#response= self.get_response(URL2,data)
			request = urllib2.Request(URL2, data)
			response = urllib2.urlopen(request)
			urll=response.geturl()
			#print urll

			if 'Logged in successfully' in str(response.read()):
				print "Succesfully logged in"

			total_feeds=len(feednames)
			a=0
			All_threads = []
			for n in range(1,NumberOfThreads+1):
				b= int(math.ceil(n*total_feeds/NumberOfThreads))
				thread = threading.Thread(target = self.feed_configure, args=(authtoken,a,b))
				thread.start()
		    		All_threads.append(thread)
				a=b
			print "Waiting..."

			for thread in All_threads:
		   		 thread.join()
			print "Alls Feeds are successfully configured "
			response.close()

if __name__=="__main__':
	feed = rss_feeds()
	feed.main()


