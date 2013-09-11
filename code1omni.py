#!/usr/bin/python
import sys
import csv
import os
import stat
import re
##*************Copyrights**************##
## OWNER: Zahin Azher Rashid
## Contact: zahin@ebryx.com
## Usage: python code1unique.py <ba_fp.csv> <md5.txt>
## Dependencies: None
##*************Thank You***************##

#***********Custom based parameters*******
sort_wrt_col_num = 2  # sort the matrix w.r.t md5sum
#*****************************************

class get_started:
	# Declare Static Variables 
	index_matched_md5 = 0
	index_unique_md5 = 0
	index_prev_analyzed_md5 = 0
	index_mal_urls = 0
	OSWeightLimit=380
	found1="Java/"

	def __init__(self,sort_wrt_col_num):
		self.sort_wrt_col_num = sort_wrt_col_num
		print "Initializing..."
	
	def __del__(self):
		#os.unlink(sort_wrt_col_num)
		s=1

	def readtxtfile(self):
		try:
			md5List=open(sys.argv[2],"r+")
		except IOError:
			print "Error Reading  text File", md5List
			sys.exit()

		md5ListSplit=md5List.read()
		md5All=md5ListSplit.split('\n')
		while '' in md5All:
			md5All.remove('')
		md5 = []
		for m in md5All:
			m=re.sub(r'\r','',re.sub(r'\t','',str(m),re.M))
			md5.append(m)
		md5List.close()
		return md5

	def read_previous_csv(self):
		with open(sys.argv[3], 'rb') as f2:
			try:
				file2_reader = csv.reader(f2, delimiter=',')
			except IOError:
				print "Error Reading csv File", f2
				sys.exit()
			md5=[]
			comments=[]
			detec=[]
			for row in file2_reader:
				md5.append(row[2])
				comments.append(row[10])
				detec.append(row[3])
                       	return (md5,comments,detec)

	def openmalfile(self):
		try:
			urlList=open(sys.argv[4],"r+")
		except IOError:
			print "Error Reading malicious urls text File", urlList
			sys.exit()

		urlListSplit=urlList.read()
		urlAll=urlListSplit.split('\n')
		while '' in urlAll:
			urlAll.remove('')
		urlList.close()
		return urlAll

	def opennonmalfile(self):
		try:
			whitelist=open(sys.argv[5],"r+")
		except IOError:
			print "Error Reading whitelisted urls text File", whitelist
			sys.exit()
		whitelist1=whitelist.read()
		whitelist2=whitelist1.split('\n')
		while '' in whitelist2:
			whitelist2.remove('')
		whitelist.close()
		return whitelist2

	def extract_url(self,header):
		if re.search(r'Host:.*?\n',str(header),re.M):
			url = re.search(r'Host:.*?\n',str(header),re.M|re.I).group()
			url = re.sub(r'Host:','',re.sub(r'\n','',re.sub(r' ','',url,re.M|re.I)))
			return url
		else:
			return 'NA'

	def malicious_urls(self,row,mal_urls,whitelist_url):
		OSweight=[]
		c=1  # malicious urls found
		d=1  # white-listed urls found
		wei=row[5]
		typ=row[4]
		header = row[11]

		#print "url",url
		val=["sum_signature_conf_non_avsuite",'+',""]
		#row.insert(12,url)
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
			if  OSweight>=self.OSWeightLimit or self.found1 in useragent:
				row[10]="ML"
				self.index_mal_urls+=1
				return (True,row)
		for mds in mal_urls:
			if mds in host:
				row[10]="ML"
				self.index_mal_urls+=1
				return (True,row)
		for wl in whitelist_url:
			if wl in host:
				row[10] = "NM"
				row[3] = "UD"
				return (False,row)
		return (False,row)	

	def if_matched(self,row,md5_from_textfile): # if md5sum is present in text file
		check = False  # md5sum does not exist in csv file
		
		for md5 in md5_from_textfile:
			if md5 in row[self.sort_wrt_col_num]:
				check=True
				return True
		if check==False:
			return False

	def match_prev_analyzed_results(self,row,md5_p,comments_p,detec_p):
		index=0
		for m in md5_p:
			if m in row[2] :
				d= detec_p[index]
				c= comments_p[index]
				if ( c=='ML' or c=='NM' or c=='ml' or c=='nm' ):
					self.index_prev_analyzed_md5+=1	
					row[3]= detec_p[index]
					row[10]= comments_p[index]
					return (True,row)
				else:
					return (False,row)
				print index1,"",m,"",detec[index],"", comments[index]
				break
			index+=1
		return (False,row) 

	def main(self,md5_from_textfile):

		with open(sys.argv[1], 'rb') as f:
			try:
				file_reader = csv.reader(f, delimiter=',')
			except IOError:
				print "Error Reading csv File", file_reader
				sys.exit()
			row_all=[]
			sep_row1=[]
			i=0
			for row in file_reader: # data is read only once
				if row[self.sort_wrt_col_num]!="md5sum":
					row_all.append(row)
				else:
					sep_row1.append(row)

			sorted_rows = sorted(row_all, key=lambda row_all: row_all[self.sort_wrt_col_num])
			sorted_rows = sep_row1 + sorted_rows

			op1="op1analyzed.csv" 
			# op2="nonmatchedmd5.txt"
			# op3="uniquemd5.txt"
			op4="op1undetected.csv"
			opfile1 = csv.writer(open(op1, 'w'), delimiter=',')
			#opfile2 = open(op2, 'w')
			#opfile3 = open(op3, 'w')
			opfile4 = csv.writer(open(op4, 'w'), delimiter=',')
			check=False # if consecutive md5sum are uneqaul
			index = 0 # index of each row
			(md5_p,comments_p,detec_p) = self.read_previous_csv()
			mal_urls=self.openmalfile()
			whitelist_url=self.opennonmalfile()
			for row in sorted_rows:
				row.insert(3,'') # insering null at 3rd index of list
				row.insert(10,'') # insering null at 10th index of list
				if index < len(sorted_rows):
					if index == len(sorted_rows)-1:
						next_md5sum = "junkvalue"
						print row
					else:
						next_md5sum = sorted_rows[index+1][sort_wrt_col_num]
					if sorted_rows[index][sort_wrt_col_num]==next_md5sum:
						check=True
					else:
						check=False
					if (check==False):  # if unique md5sum 
						self.index_unique_md5+=1
						#opfile3.write(row[sort_wrt_col_num]+'\n')
						row.insert(12,'')
						if row[self.sort_wrt_col_num]=="md5sum":
							row[12] = "Host"
							opfile4.writerow(row)
							
						else:
							value = self.if_matched(row,md5_from_textfile)
							if value == True:  # if matched
								header = row[11]
								url = self.extract_url(header)    # retrieve url from header
								row[12] = url
								(value1,row) = self.malicious_urls(row,mal_urls,whitelist_url)
								if value1 == True:
									opfile1.writerow(row) # Analyzed
								else:	
									(value2,row) = self.match_prev_analyzed_results(row,md5_p,comments_p,detec_p)
									if value2 == True:
										opfile1.writerow(row) # Analyzed
									else:
										opfile4.writerow(row) # Undetected
								self.index_matched_md5+=1
								if ((self.index_matched_md5%1000) == 0 ):
									print "Files Analyzed so far =>",self.index_matched_md5
								#print row[sort_wrt_col_num]
							else:
								#print row[sort_wrt_col_num]
								#opfile2.write(row[sort_wrt_col_num]+'\n')
								s=0

				index+=1
			print "Total Unique md5sum :",	self.index_unique_md5
			print "Total Matched md5sum :", self.index_matched_md5
			print "Total Previous analyzed md5sum :",self.index_prev_analyzed_md5
			print "Total Malicious urls associated :",self.index_mal_urls
			print "Total Analyzed Files :",self.index_prev_analyzed_md5+self.index_mal_urls
			print "Output is saved to op1analyzed.csv and op1undetected.csv Files"
		f.close() # Be safe

if __name__ == '__main__':	
	if len(sys.argv)!=6:
		print "     Incorrect input paramaters    "
		print "*********How to run the script*****"
		print "python code1unique.py <ba_fp.csv> <md5.txt> <prev.csv> <mal*.txt> <whit*.txt>"
		sys.exit(1)

	Run = get_started(sort_wrt_col_num) # class object
	md5_from_textfile = Run.readtxtfile()
	Run.main(md5_from_textfile)
