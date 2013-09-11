#!/usr/bin/python
#################  How to run the Script ######################              
#Step1: Copy your .csv file in this folder
#Step2: Run code3pasteAllResult.py Script
#       terminal input: $python code1paste-DetectedResults.py  VT_undetected.csv detected.csv noOfProfiles
###############################################################
import sys
import csv
import os
import stat
import re
##*************Copyrights**************##
## OWNER: Zahin Azher Rashid
## Contact: zahin@ebryx.com
## Usage: python url_query.py <path to file>
## Dependencies: None
##*************Thank You***************##

class pasteDetected:

	count_detected = 0
	count_undetected = 0
	count_notFound = 0

	def __init__(self):
		print "Initializing..."

	def main(self):

		with open(sys.argv[2], 'rb') as f2:
			try:
				file2_reader = csv.reader(f2, delimiter=',')
			except IOError:
				print "Error Reading csv File", f2
				sys.exit()
			md5=[]
			weight=[]
			m_ids=[]
			profile_name=[]
			is_mal=[]
			signame=[]

			countw=0
			for row in file2_reader:
				if countw==0:
					countw=1
				else:
					if not ("md5sum" in row[0] or "weight" in row[1]):
						valwei=row[2]
						if ('+' in row[2]):
							valwei= 1000
						md5.append(row[0])
						m_ids.append(row[1])
						weight.append(valwei)
						profile_name.append(row[3])
						is_mal.append(row[4])
						signame.append(row[5])

		        # Malware Signatures to detect TP
			"""try:
				siglist=open("malwaresignatures.txt","r+")
			except IOError:
				print "Error Reading malware signatures text File", 
				sys.exit()
			urlListSplit=siglist.read()
			Signames_MAL=urlListSplit.split('\n')
			while '' in Signames_MAL:
				Signames_MAL.remove('')
			siglist.close()
			#print "Signames_MAL: ",Signames_MAL"""

			"""Signames_MAL=['Trojan.KorAd','Backdoor.Xtrat.A','Trojan.SpyEyes','Backdoor.APT.LV','Trojan.Ruskill',
	'FE_SuspiciousResource_Icon_PDF_1','Rogue.AV.ogkr','Worm.Gamarue.B']"""
			Signames_MAL=['asd.asdf']

			md5.append("junk") ; md5.append("junk1") 

		files_count= len(md5)  # total count of files
		n1= "app_detected.csv"
		optfile= csv.writer(open(n1, 'w'), delimiter=',')
		n2= "app_NF.csv"
		optfile2= csv.writer(open(n2, 'w'), delimiter=',')
		n3= "op1analyzed.csv"
		optfile3= csv.writer(open(n3, 'a+'), delimiter=',')
		with open(sys.argv[1], 'rb') as f:
			try:
				file1_reader = csv.reader(f, delimiter=',')
			except IOError:
				print "Error Reading csv File", f
				sys.exit()
			index1=1
			for row in file1_reader:
				a=1   #  check md5 exists in detected.csv file
				index=0   # it corresponds to index of each hash
				profile_count=int(sys.argv[3])  # total profiles limit e.g 1,2,3
				row.insert(13,'')
				if "md5sum" in row[2]:
					row[13] = "Static Info"
					optfile.writerow(row)
				else:
					static_info = ''
			
					for m in md5:
						if md5[index] == row[2]:	
							a+=1
							val=["weight",'+',""] # To make sure it is int
							totalWeight=[] # make a list of total weights across each 
							is_mal_all=''
							profile_name_all=''
							if index < (files_count-1):
								profile_countcheck=1
								totalWeight.append(weight[index])
								profile_name_all = 'profile '+profile_name[index]+' ; M_id = '+m_ids[index]+' => '+weight[index]+'  ; '+signame[index]
						
								while (md5[index] == md5[index+1]):	
									if int(profile_countcheck) == profile_count:
										break
									totalWeight.append(weight[index+1])
									profile_name_all = profile_name_all+'\n'+'profile '+profile_name[index+1]+' ; M_id = '+m_ids[index+1]+' => '+weight[index+1]+'  ; '+signame[index+1]
									profile_countcheck+=1
				            				index+=1  # very important step
							#print profile_name_all
					
							row[13]=profile_name_all
							#print totalWeight , " ; " , len(totalWeight)

							# Check for SIG match, if malicious insert in undec+TP file
							if signame[index] in Signames_MAL:
								row[3]='DT'
								row[10]='ML'
								optfile3.writerow(row)
								self.count_detected+=1
								break

							if len(totalWeight)>0:  # if result of at least one profile exist 
								if totalWeight[0] not in val:
									#maxValue = max(totalWeight)
									#print "len(totalWeight)", len(totalWeight)
									i = 1 ; # index corresponding each weight
									M = int(totalWeight[0]) # max value of list
									while i < (len(totalWeight)) :
										if int(totalWeight[i]) > M:
											M = int(totalWeight[i])
										i+=1
									maxValue = M	
									#print m," ; maxValue ",maxValue
									if maxValue >= 100:
										#print m," ; maxValue ",maxValue
										row[3]='DT'
										optfile.writerow(row)
										self.count_detected+=1
									else:   # if it is undetected
										row[3]='UD'
										row[10]='NM'
										optfile3.writerow(row)
										self.count_undetected+=1
							else :
								maxValue = weight[index]
								maxValue = int(maxValue)
								#print m," ; maxValue ",maxValue
								if int(maxValue) >= 100:  # if it is detected
									#print m," ; maxValue ",maxValue
									row[3]='DT'
									optfile.writerow(row)
									self.count_detected+=1
								else:   # if it is undetected
									row[3]='UD'
									row[10]='NM'
									optfile3.writerow(row)
									self.count_undetected+=1
							#optfile.writerow(row)
							break

						index+=1
					if a == 1:  # if it is not found
						row[3]='NF'
						self.count_notFound+=1
						optfile2.writerow(row)

		#print "count ",files_count
		print "Total detected Files =>",self.count_detected
		print "Total undetected Files =>",self.count_undetected
		print "Total notfound Files =>",self.count_notFound
		print "Output Files are op1analyzed.csv, app_detected.csv and app_NF.csv"
		f2.close()
		f.close()

if __name__ == '__main__':
	if len(sys.argv)!=4:
		print "     Incorrect input paramaters    "
		print "*********How to run the script*****"
		print "python code1paste-DetectedResults.py  VT_undetected.csv detected.csv noOfProfiles"
		sys.exit(1)
	VT_DT = pasteDetected()
	VT_DT.main()
