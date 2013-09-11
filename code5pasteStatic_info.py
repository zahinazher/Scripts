#!/usr/bin/python
#################  How to run the Script ######################              
# $python code1paste-DetectedResults.py  app_detected.csv static_info.txt network.csv
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

class Static:

	def __init__(self):
		print "Initializing..."

	def main(self):
		
		try:
			f = open(sys.argv[2] , 'r')  # static_info.txt
			data = f.read()
			#print data
		except:
			print "text file read error"

		with open(sys.argv[3], 'rb') as f2:  # network.csv file
			try:
				file2_reader = csv.reader(f2, delimiter=',')
			except IOError:
				print "Error Reading csv File", f2
				sys.exit()
			md5_ntwrk=[]
			bot_host=[]
			count=0
			for row in file2_reader:
				if count==0:
					count+=1
				else:
					md5_ntwrk.append(row[0])
					bot_host.append(row[1])
				
		total_md5_net=len(md5_ntwrk)

		n1= "app_detected-stat.csv"
		optfile= csv.writer(open(n1, 'w'), delimiter=',')

		with open(sys.argv[1], 'rb') as f:
			try:
				file1_reader = csv.reader(f, delimiter=',')
			except IOError:
				print "Error Reading csv File", f
				sys.exit()
			index1=1
			dt_count =0; ud_count = 0 ; nf_count=0
			count_md5 = 0 # Total Files 
			for row in file1_reader:
				a=1   #  check md5 exists in static-info.txt file
				index=0   # it corresponds to index of each hash
				if ((count_md5 % 50) == 0):
					print "Files Analyzed so far =>",count_md5
			
				if "md5sum" in row[2]:
					optfile.writerow(row)
				else:
					md5 = row[2]
					#row.insert(13,'')
					information = row[13]
					#print "md5 : ",md5
					if (re.search(re.escape(md5)+r'.*?Section\(s\)',str(data),re.I|re.M|re.DOTALL)):
						info = re.search(re.escape(md5)+r'.*?Section\(s\)',str(data),re.I|re.M|re.DOTALL).group()
						orig_filename='';file_version='';comp_name='';file_version='';product_name='';file_description='';
						signer_info=''
						check=False # if File info is not present 
						if( re.search(r'Orignal File name.*',str(info)) ):
							orig_filename = re.search(r'Orignal File name.*',str(info)).group()
							check=True
							#print orig_filename
						if( re.search(r'File Version.*',str(info)) ):
							file_version = re.search(r'File Version.*',str(info)).group()
							#print file_version
						if( re.search(r'Company Name.*',str(info)) ):
							comp_name = re.search(r'Company Name.*',str(info)).group()
							#print comp_name
						if( re.search(r'Product Name.*',str(info)) ):
							product_name = re.search(r'Product Name.*',str(info)).group()
							#print product_name
						if( re.search(r'File Description.*',str(info)) ):
							file_description = re.search(r'File Description.*',str(info)).group()
							#print file_description
				
						static_info = orig_filename+'\n'+file_version+'\n'+comp_name+'\n'+product_name+'\n'+file_description
						check1 = False
						if( re.search(r'Name of signer.*',str(info)) ):
							signers = re.findall(r'Name of signer.*',str(info))
							check1 = True
							for s in signers:
								signer_info = signer_info + s + '\n'
							static_info = signer_info+static_info

						if check==True:
							information = information +'\n'+ static_info
						elif check==False and check1==True:
							information = information +'\n'+ signer_info
					

						index_net=0

						for m in md5_ntwrk:
							if m == row[2]:
								if index_net < (total_md5_net-1):
									net_host = bot_host[index_net]
									while (md5_ntwrk[index_net]==md5_ntwrk[index_net+1] and (index_net+1)==total_md5_net):
										net_host = net_host + '\n' + bot_host[index_net+1]
										index_net+=1
									Bot_comm = 'Bot_communication:\n'+net_host
									information = information + '\n'+Bot_comm
									#print information
								break
						
							index_net+=1
						row[13]=information
						a=0	
						optfile.writerow(row)

					index+=1
					if a == 1:  # if it is not found
						nf_count+=1
						optfile.writerow(row)
				count_md5+=1
		print "Total Files :",count_md5
		print "Output is saved to app_detected.csv File"
		os.rename('app_detected-stat.csv','app_detected.csv')
		f.close()

if __name__ == '__main__':
	if len(sys.argv)!=4:
		print "     Incorrect input paramaters    "
		print "*********How to run the script*****"
		print "python code1paste-DetectedResults.py  app_detected.csv static_info.txt network.csv"
		sys.exit(1)
	St = Static()
	St.main()
