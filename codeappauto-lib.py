import urllib2
import urllib
import cookielib
import sys
import os
from BeautifulSoup import BeautifulSoup
import json
import re
import string
import csv
import math
import httplib
import ssl
import time
import datetime

##*************Copyrights**************##
## OWNER: Zahin Azher Rashid
## Contact: zahin@ebryx.com
## Usage: python codeappauto-lib.py <path to file>
## Dependencies: BeautifulSoup
##*************Thank You***************##

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPRedirectHandler(),urllib2.HTTPCookieProcessor(cj),urllib2.HTTPSHandler())
urllib2.install_opener(opener)

class appliance:

	def get_auth_token(self,response):
		try:
			soup = BeautifulSoup(response)
			auth_token = soup.find('input', type='hidden', attrs={'name': 'authenticity_token'})
			authtoken = auth_token['value']
			authtoken = str(authtoken)
			return authtoken
		except:
			return 'NA'

	def get_cookie(self,response):
		try:
			info = response.info()
			cookie = re.search(r'Set-Cookie:.*?;',str(info)).group()
			cookie = re.sub(r'Set-Cookie: _session_id=','',re.sub(r';','',cookie))
			return cookie
		except:
			return 'NA'

	def check_connectivity(self):
		try:
			urllib.request.urlopen('http://www.google.com', timeout=5)
			return True
		except urllib2.HTTPError as er:
			return False

	def get_response(self,URL,data):
		try:
			request = urllib2.Request(URL,data)
			response = urllib2.urlopen(request)
			return response
		except urllib2.HTTPError as e:
			print "HTTP error" , e.code
		except:
			print "urllib.request.URLError"
			while (self.check_connectivity() == False):
				pass
	
	def get_eventcluster_id(self,tb):
		if (re.search(r'render_event_cluster.*',str(tb))):
			event_cluster = re.search(r'render_event_cluster.*',str(tb)).group()
			event_cluster = re.search(r'\(.*\)',event_cluster).group()
		else:
			event_cluster = 'NA'
		if (re.search(r'\(.*?\,',event_cluster)):
			event_cluster1 = (re.search(r'\(.*?\,',event_cluster)).group()
			event_cluster1 = re.sub(r'\,','',re.sub(r'\(','',re.sub(r"\'",'',event_cluster1)))
		else:
			event_cluster1 = 'NA'
		if (re.search(r'\,.*?\,',event_cluster)):
			event_cluster2 = (re.search(r'\,.*?\,',event_cluster)).group()
			event_cluster2 = re.sub(r'\,','',re.sub(r"\'",'',event_cluster2))
		else:
			event_cluster2 = 'NA'

		return (event_cluster1,event_cluster2)

	def get_status_information(self,resp1):
		soup = BeautifulSoup(''.join(resp1))
		status_all=[]  # detection status
		malware_ids = [] 
		event_cluster1_all = []
		event_cluster2_all = []
		sig_name_all = []  # signatures names in all profiles specified
		profile_names = []  
		count=0 # check on number of profiles
		df=1
		noOfProfiles = 3 # No. of profiles to check status on
		try:
			tbody = soup.findAll('tbody')
			for tb in tbody:
				if (len(tb)>0 and count < noOfProfiles):
					if (re.search(r'win.*',str(tb))):
						tt4 = re.search(r'win.*nbsp;',str(tb)).group()
						tt4 = re.sub(r'&nbsp;','',tt4)
						profile_names.append(tt4)
					tt= re.findall(r'<td>.*?</td>',str(tb))	
					tt1 = tt[0]
					tt1 = re.sub(r'<td>','',re.sub(r'</td>','',tt1))
					malware_ids.append(tt1)	
					tt2 = tt[1]
					tt2 = re.sub(r'<td>','',re.sub(r'</td>','',tt2))
					status_all.append(tt2)
					tt3 = tt[3]
					tt3 = re.sub(r'<td>','',re.sub(r'</td>','',tt3))
					if (re.search(r'>.*<',tt3)):
						tt3 = re.search(r'>.*<',tt3).group()
						tt3 = re.sub(r'>','',re.sub(r'<','',tt3))
						sig_name_all.append(tt3)
					if (re.search(r'render_event_cluster.*',str(tb))):
						(event_cluster1,event_cluster2) = self.get_eventcluster_id(tb)
						event_cluster1_all.append(event_cluster1)
						event_cluster2_all.append(event_cluster2)
				count+=1
			try:
				malware_id = malware_ids[0]
				sig_name = sig_name_all[0]
				event_cluster_id1 = event_cluster1_all[0]
				event_cluster_id2 = event_cluster2_all[0]
				cnt = 0 # Number of profiles check 
				pf_id_st = ""  # profile name + malware id+ status
				for v in status_all:
					d="UD"
					pf_id_st = pf_id_st+profile_names[cnt]+" : "+malware_ids[cnt]+" => "+v+"\n"
					cnt+=1
					if 'Y' in v:			
						d="DT"
				return (d,malware_id,sig_name,event_cluster_id1,event_cluster_id2,pf_id_st)
			except Exception as e:
				print "exception in get_status:",e	
				return	("NA","NA","NA","NA","NA","NA")	

		except Exception as ee:
			print "Error in get_status: ", ee
			return ("NA","NA","NA","NA","NA","NA")

	def filter_searched_strings(self,tr_tag,s1,s2):
			t = (re.search(s1,str(tr_tag))).group()
			t = re.sub(r' ','',re.sub(r'</tol>','',t))
			orig_filename = re.sub(s2,'',t)
			orig_filename = s2+orig_filename
			return orig_filename
		
	def get_File_info(self,resp2):
		soup = BeautifulSoup(''.join(resp2))
		body = soup.find('events')
		bot_comm_host = []
		if ( re.search(r'hostname.*',str(body)) ):
			host = re.findall(r'<hostname.*',str(body))
			for h in host:
				h = re.sub(r'<hostname>','',re.sub('</hostname>','',str(h)))
				bot_comm_host.append(h)
			print bot_comm_host

		tol = body.findAll('tol')
		orig_filename='NA'; file_version='NA'; company_name='NA';
		product_name='NA'; file_description='NA';name_of_signer='Unsigned'
		c1=0;c2=0;c3=0;c4=0;c5=0;c6=0;
		for tr_tag in  tol:
			if c1 ==0:
				if( re.search(r'Orignal File name.*',str(tr_tag)) ):
					orig_filename = self.filter_searched_strings(tr_tag,'Orignal File name.*','OrignalFilename:')
					c1=+1
			if c2 ==0:
				if( re.search(r'File Version.*',str(tr_tag)) ):
					file_version = self.filter_searched_strings(tr_tag,'File Version.*','FileVersion:')
					c2+=1
			if c3 ==0:	
				if( re.search(r'Company Name.*',str(tr_tag)) ):
					company_name = self.filter_searched_strings(tr_tag,'Company Name.*','CompanyName:')
					c3+=1
			if c4 ==0:
				if( re.search(r'Product Name.*',str(tr_tag)) ):
					product_name = self.filter_searched_strings(tr_tag,'Product Name.*','ProductName:')
					c4+=1
			if c5 ==0:
				if( re.search(r'File Description.*',str(tr_tag)) ):
					file_description = self.filter_searched_strings(tr_tag,'File Description.*','FileDescription:')
					c5+=1
			if c6 ==0:
				if( re.search(r'Name of signer.*',str(tr_tag)) ):
					name_of_signer = self.filter_searched_strings(tr_tag,'Name of signer.*','Nameofsigner:')
					c6+=1

			File_information = (name_of_signer+'\n'+orig_filename+'\n'+file_version
					+'\n'+company_name+'\n'+product_name+'\n'+file_description)
		return 	File_information


def main():
	
	if len(sys.argv)==2:
		filename = sys.argv[1]
		
		time1 = datetime.datetime.time(datetime.datetime.now())	
		APP = appliance()
		url = 'https://10.5.6.134/login/login'
		response = APP.get_response(url,None)
		authtoken=APP.get_auth_token(response)
		
		headers = {'Host':'10.5.6.134',
			'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'Accept-Language':'en-US,en;q=0.5',
			'Accept-Encoding':'gzip, deflate',
			'Referer':'https://10.5.6.134/malware_analysis/analyses',
			'Connection':'keep-alive',
			'Content-Type':'application/x-www-form-urlencoded'}

		a = """\xE2\x9C\x93"""
		username='admin'
		password='admin'
		details={ 'authenticity_token': authtoken,'user[account]' : username, 'user[password]' : password}
		data = urllib.urlencode(details)
		response = APP.get_response(url,data)
		try:
			resp = response.read()
			if "Logged in as" in resp:
				print "logged in succesfully as admin : " + a
		except Exception as e:
			print "Login failed:",e
		url = 'https://10.5.6.134/malware_analysis/analyses'
		response = APP.get_response(url,None)
		#print response.read()
		url3 = 'https://10.5.6.134/manual/date_time'
#POST /malware_analysis/update_filter HTTP/1.1
		app_info= csv.writer(open("app_detected-info.csv", 'w'), delimiter=',')

		with open(filename, 'rb') as f3:
			try:
				urlAll5_reader = csv.reader(f3, delimiter=',')
			except IOError:
				print "Error Reading csv File", f3
				sys.exit()
			countmd5 = 0
			for row in urlAll5_reader:
				m = row[2]
				print "md5sum"+str(countmd5)+": "+str(m)
				row.insert(13,'')
				details={ 'authenticity_token': authtoken,
					'filter':'Set',
					'ma_filter_text':m,
					'ma_filter_col':'md5sum',
					'ma_username':'All',
					'_':''}
				data = urllib.urlencode(details)
				try:
					#response = APP.get_response(url1,data)
					#resp1 = response.read()  # result of md5 search
					print authtoken
					url1 = 'https://10.5.6.134/malware_analysis/update_filter'
					request = urllib2.Request(url1,data)
					response = urllib2.urlopen(request)
					print response.read()
					(status,m_id,sig_name,e_id1,e_id2,pf_id_st) = APP.get_status_information(resp1) 
					print "e_id1",e_id1
					print "e_id2",e_id2
					if (e_id1 !='NA'):
						if (e_id2=='NA'):
							e_ids=e_id1
						else:
							e_ids=e_id1+','+e_id2
						f_info = pf_id_st+"sig_name:"+sig_name+"\n"
						row[13] = f_info 
						details={ 'authenticity_token': authtoken,'_':''}
						url2 = 'https://10.5.6.134/event_stream/events_in_xml?events='+e_ids2+'&arow='+m_id+'&noxsl=y'
						#https://10.5.6.134/event_stream/events_in_xml?events=13934,13935&arow=7771&noxsl=y
						try:
							response = APP.get_response(url2,data)
							resp2 = response.read()  # result of additional info
							f_info = APP.get_File_info(resp2)
							f_info = pf_id_st+"sig_name:"+sig_name+"\n"+f_info
							row[13] = f_info 
							#print f_info
						
							f = open("resp_appl2.txt" , "w")
							f.write(resp2)
							app_info.writerow(row)
						except Exception as e:
							app_info.writerow(row)
							print "No resp2 data:",e			
				except Exception as e:
					app_info.writerow(row)
					print "No resp1 data:",e
			countmd5+=1

		time2 = datetime.datetime.time(datetime.datetime.now())	
		print "Starting time:",time1
		print "Ending time:",time2
	else:
		print "Usage: python url_query.py <path to file>"
		sys.exit()

if __name__ == '__main__':	
	main()
