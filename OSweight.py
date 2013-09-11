#!/usr/bin/python
#################
#                    How to run the Script
#Step1: run code2malurls.py to detect md5's with malicious url's
#	command terminal input: $ python code2malurls.py op1prevdetetced.csv maliciousurls.txt whitelistedurls.txt
#	output files are "VT_undetected.csv"
#################


import sys
import csv
import os
import stat
import re
#To run this code : $python code2malurls.py op1prevdetetced.csv maliciousurls.txt whitelistedurls.txt

n1= "VT_notFoundn.csv"
mal= csv.writer(open(n1, 'w'), delimiter=',')
###### These following values can be changed as desired 
OSWeightLimit=180
OSWeightlimit1=300
found1="directdownloader.com"
######


with open(sys.argv[1], 'rb') as f3:
	try:
		urlAll5_reader = csv.reader(f3, delimiter=',')
	except IOError:
		print "Error Reading csv File", f3
		sys.exit()
	
	index=0
	index1=0	
	OSweight=[]
	for row in urlAll5_reader:
		c=1
		d=1
		e=1
		wei=row[5]
		typ=row[4]
		header=row[11]
		host=re.search(r'Host:.*?\n',header,re.M|re.I)
		if host:
			host=host.group()
		else:
			host=''
		val=["sum_signature_conf_non_avsuite",'+',""]
		if wei not in val:
			OSweight=int(wei)
			if  (OSweight==OSWeightLimit and typ=="zip") or (found1 in host) or (OSweight>OSWeightlimit1):
				row[10]="ML"
				mal.writerow(row)
				index+=1
				print index,"",row[2],"",typ,"",wei
				e+=1
		if e==1:
			mal.writerow(row)

f3.close()             
