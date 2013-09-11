
import urllib2
import urllib
import cookielib
import sys
import os
from BeautifulSoup import BeautifulSoup
import re
import string
import csv
import math
import httplib
import ssl
import time
#import mechanize
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

##*************Copyrights**************##
## OWNER: Zahin Azher Rashid
## Contact: zahin@ebryx.com
## Usage: python url_query.py <path to file>
## Dependencies: BeautifulSoup
##*************Thank You***************##

"""
apt-get install python-bs4
soup = BeautifulSoup(html_doc)
print(soup.prettify())
get_url_contents(r[0]).decode('ascii').encode('ascii', 'ignore')
sudo pip install -U selenium
"""

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPRedirectHandler(),urllib2.HTTPCookieProcessor(cj),urllib2.HTTPSHandler())
urllib2.install_opener(opener) # globally it can be used with urlopen
browser=webdriver.Firefox()
class appliance:


	def readfile(self,filename):
		with open(filename, 'rb') as f:
		    reader = csv.reader(f)
		    md5sum = []
		    try:
			for row in reader:
			    md5sum.append(row[0])
			return (md5sum)
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
		if 'Set-Cookie' in info:
		  	cookie_all = info['Set-Cookie']
			#print "cookie_all",cookie_all
			cookie = cookie_all[:string.find(cookie_all, ';')]
			#print "cookie is present "
			return cookie		
		else:
			print "no cookie"

	def get_response(self,URL,data,headers):
		try:
			request = urllib2.Request(URL, data)
			response = urllib2.urlopen(request)
		except urllib2.HTTPError as e:
			print "HTTP error" , e.code		
		return response

	#***********retriving status information********
	def get_status_information(self,resp1):
		try:
			soup = BeautifulSoup(''.join(resp1))
			body = soup.find('body')

			tbody = body.findAll('tbody')
			tr=[]
			count=0
			df=1
			for tb in tbody:
				if len(tb[8])>0:
					if count in [4,6,8]:  # check in first 3 profile
						tt= re.findall(r'<td>.*?</td>',str(tb))	
						tr.append(tt)
				elif len(tb[6])>0:
					if count in [4,6]:  # check in first 3 profile
						tt= re.findall(r'<td>.*?</td>',str(tb))	
						tr.append(tt)
				elif len(tb[4]):
					if count in [4]:  # check in first 3 profile
						tt= re.findall(r'<td>.*?</td>',str(tb))	
						tr.append(tt)
				else:
					df=2
				count+=1
		
			if df == 1:
				for v in tr:
					for v1 in v[1]:
						d="UD"
						#print v1
						if 'Y' in v1:
							print v1			
							d="DT"
							break
			else:
				d="NA"
			return d
		except Exception as ee:
			print ee

	def get_signer_information(self,resp2):
		soup = BeautifulSoup(''.join(resp2))
		body = soup.find('body')
		tr = body.findAll('tr')
		sign = []
		signer = "NA"
		for t in tr:
			if( re.search(r'Nameofsigner.*?/>',str(t)) ):
				print "signer exists"
				tt = re.search(r'Nameofsigner.*?/>',str(t))
				sign.append(tt.group())
				signer = sign[0]
				signer = re.sub(r'Nameofsigner:','',re.sub(r'<br />','',signer))
				break	
		print "signer",signer
		return signer

	def get_File_info(self,resp2):
		soup = BeautifulSoup(''.join(resp2))
		body = soup.find('body')
		tr = body.findAll('tbody')
		tr_tag = tr[4]
		orig_filename='NA'; file_version='NA'; company_name='NA';
		product_name='NA'; file_description='NA';name_of_signer='NA'
		if( re.search(r'OrignalFilename.*',str(tr_tag)) ):
			t = (re.search(r'OrignalFilename.*',str(tr_tag))).group()
			orig_filename = re.sub(r'OrignalFilename:','',re.sub(r'<br />','',t))
			orig_filename = ('OrignalFilename: '+orig_filename)
			#print orig_filename
		if( re.search(r'FileVersion.*',str(tr_tag)) ):
			t = (re.search(r'FileVersion.*',str(tr_tag))).group()
			file_version = re.sub(r'FileVersion:','',re.sub(r'<br />','',t))
			file_version = ('file_version: '+file_version)
			#print file_version	
		if( re.search(r'CompanyName.*',str(tr_tag)) ):
			t = (re.search(r'CompanyName.*',str(tr_tag))).group()
			company_name = re.sub(r'CompanyName:','',re.sub(r'<br />','',t))
			company_name = 'company_name: '+company_name
			#print company_name
		if( re.search(r'ProductName.*',str(tr_tag)) ):
			t = (re.search(r'ProductName.*',str(tr_tag))).group()
			product_name = re.sub(r'ProductName:','',re.sub(r'<br />','',t))
			product_name = 'product_name: '+product_name
			#print product_name
		if( re.search(r'FileDescription.*',str(tr_tag)) ):
			t = (re.search(r'FileDescription.*',str(tr_tag))).group()
			file_description = re.sub(r'FileDescription:','',re.sub(r'<br />','',t))
			file_description = 'file_description: '+file_description
			#print file_description
		if( re.search(r'Nameofsigner.*',str(tr_tag)) ):
			t = (re.search(r'Nameofsigner.*',str(tr_tag))).group()
			name_of_signer = re.sub(r'Nameofsigner:','',re.sub(r'<br />','',t))
			name_of_signer = 'Name of signer: '+name_of_signer
			#print name_of_signer
		File_information = (name_of_signer+'\n'+orig_filename+'\n'+file_version
				+'\n'+company_name+'\n'+product_name+'\n'+file_description)
		return 	File_information

	def get_signature_info(self,resp2):
		soup = BeautifulSoup(''.join(resp2))
		body = soup.find('body')
		tbody = body.findAll('tbody')
		#print tbody
		tbody = tbody
		bot_comm='NA';call_back='NA'
		for tb in tbody:
			try:
				if( re.search(r'Bot Communication Details.*',str(tb)) ):
					g = re.search(r'Bot Communication Details.*',str(tb)).group()
					g = re.search(r'<i>.*</i>',str(tb)).group()
					bot_comm = re.sub(r'<i>','',re.sub(r'</i>','',g))
					bot_comm = 'Bot Communication: '+bot_comm
					#print bot_comm
					break
			except:
				pass
		for tb in tbody:
			try:
				if( re.search(r'Callback communication.*',str(tb)) ):
					g = re.search(r'Callback communication.*',str(tb)).group()
					g = re.search(r'<i>.*</i>',str(tb)).group()
					call_back = re.sub(r'<i>','',re.sub(r'</i>','',g))
					call_back = 'Bot Communication: '+bot_comm
					#print call_back
					break
			except:
				pass
		return (bot_comm , call_back )

	def search_md5sum(self,m):
		try:
			browser.get("https://10.5.6.134/malware_analysis/analyses")
			assert "Malware" in browser.title
			ele4 = browser.find_element_by_id("ma_filter_text")
			ele4.clear()
			ele4.send_keys(m)	
			ele5 = browser.find_element_by_id("ma_filter_col")
			ele5.send_keys("Md5sum")
			ele6 = browser.find_elements_by_class_name("green")
			ele6[1].click()
			browser.get("https://10.5.6.134/malware_analysis/analyses")
			assert "Malware" in browser.title
			print "md5sum filter on"

			resp1 = browser.page_source.encode('ascii', 'ignore')
			ele7 = browser.find_elements_by_tag_name("img")

			ele7[5].click()
		
			print "chk"		
			#browser.get("https://10.5.6.134/malware_analysis/analyses")
			while "Change Detail" not in browser.page_source:
				pass
			print "OS alerts page expand"
			resp2 = browser.page_source.encode('ascii', 'ignore')
	

		
			f=open("test.txt", "w")
			f.write(resp2)
			f.close()
		
			st = self.get_status_information(resp1)	
			signer = self.get_signer_information(resp2)
			(bot_comm , call_back ) = self.get_signature_info(resp2)
			file_info = self.get_File_info(resp2)
			print file_info
			print bot_comm
		except NoSuchElementException:
			print "no such element"
			st="NA"
			signer="NA"
			pass
		except Exception as ee:
			print "except" ,m
			print ee
			st="NA"
			signer="NA"
			pass
		return (st,signer)

def main(): 
	filename=sys.argv[1]
	APP = appliance()
	#md5=APP.readfile(filename)
	md5 = ['2c5c86e0147d213ff80acca2eeb222ad']
	print "md5",md5

	
	index=0
	status = []
	signer_info = [] 

	browser.get("https://10.5.6.134/login/login")
	ele1 = browser.find_element_by_id("user_account")
	ele1.send_keys("admin")
	ele2 = browser.find_element_by_id("user_password")
	ele2.send_keys("admin")
	ele3 = browser.find_element_by_id("logInButton")
	ele3.click()

	if "Logged in as" in browser.page_source:
		print "Successfully logged in"
	counta=1
	for m in md5:
		(st,signer)=APP.search_md5sum(m)
		counta+=1
		status.append(st)
		signer_info.append(signer)
		
	print status
	print signer_info
		#ele5.send_keys(Keys.RETURN)
	index=0
	#op = csv.writer(open(name, 'w'), delimiter=',')
	for md in md5:

		#op.writerow([md,signer_info[index]])
		index+=1
	#browser.close()

if __name__ == '__main__':
	
	main()	
