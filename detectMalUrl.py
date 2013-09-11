#!/usr/bin/python
#################
#                    How to run the Script
#Step1: Copy the new .csv file and the last week .csv file in the folder where the codes are placed
#Step2: run code1prevdetectedmd5.py to retrieve the result of last week md5's if it exists
#	command terminal input: $ python code1prevdetectedmd5.py newfile.csv prevfile.csv
#	output file is "op1prevdetetced.csv"
#Step3: run code2malurls.py to detect md5's with malicious url's
#	command terminal input: $ python code2malurls.py op1prevdetetced.csv maliciousurls.txt whitelistedurls.txt
#	output files are "op2maliciousUrls.csv" and "op2nonmaliciousUrls.csv"
#Step4: Now submit this output file on VT
#################
#               Important Note
# row[2] contains md5sum
# row[3] contains applaince detection remarks 'Detected/DT' or 'Undetected/UD'
# row[10] contains your remarks 'ML' or 'NM'
#################

import sys
import csv
import os
import stat
import re
#To run this code : $python code2malurls.py op1prevdetetced.csv maliciousurls.txt whitelistedurls.txt

###### These following values can be changed as desired 
OSWeightLimit=380
found1="Java/"
######

def openmalfile():
	try:
		urlList=open(sys.argv[2],"r+")
	except IOError:
		print "Error Reading malicious urls text File", urlList.txt
		sys.exit()

	urlListSplit=urlList.read()
	urlAll=urlListSplit.split('\n')
	while '' in urlAll:
		urlAll.remove('')
	urlList.close()
	return urlAll

def opennonmalfile():
	try:
		whitelist=open(sys.argv[3],"r+")
	except IOError:
		print "Error Reading whitelisted urls text File", whitelist.txt
		sys.exit()
	whitelist1=whitelist.read()
	whitelist2=whitelist1.split('\n')
	while '' in whitelist2:
		whitelist2.remove('')
	whitelist.close()
	return whitelist2

def main():
	urlAll=openmalfile()
	whitelist2=opennonmalfile()
	with open(sys.argv[1], 'rb') as f3:
		try:
			urlAll5_reader = csv.reader(f3, delimiter=',')
		except IOError:
			print "Error Reading csv File", f3
			sys.exit()
		n1= "s2op2maliciousUrls.csv"
		n2= "s2op2nonmaliciousUrls.csv"
		mal= csv.writer(open(n1, 'w'), delimiter=',')
		nonmal= csv.writer(open(n2, 'w'), delimiter=',')
		index=0
		index1=0	
		OSweight=[]
		for row in urlAll5_reader:
			c=1
			d=1
			e=1
			wei=row[5]
			typ=row[4]
			val=["sum_signature_conf_non_avsuite",'+',""]
			header=row[11]
			host=re.search(r'Host:.*?\n',header,re.M|re.I)
			useragent=re.search(r'User-Agent:.*?\n',header,re.M|re.I)
			if host:
				host=host.group()
			else:
				host=''
			if useragent:
				useragent=useragent.group()
			else:
				useragent=''
			if wei not in val:
				OSweight=int(wei)
				if  OSweight>=OSWeightLimit or found1 in useragent:
					row[10]="ML"
					mal.writerow(row)
					index+=1
					print index,"",row[2],"",typ,"",wei
					e+=1
			if e==1:
				for mds in urlAll:
					if mds in host:
						row[10]="ML"
						mal.writerow(row)
						c+=1
						index+=1
						print index,"",mds
						break
				for wl in whitelist2:
					if wl in host:
						row[10] = "NM"
						row[3] = "UD"
						nonmal.writerow(row)
						d+=1
						index1+=1
						#print index1,"",wl
						break
				if c==1 and d==1:
					nonmal.writerow(row)
	f3.close()  
main()           
