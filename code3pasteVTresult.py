#!/usr/bin/python
import sys
import csv
import os
import stat
##*************Copyrights**************##
## OWNER: Zahin Azher Rashid
## Contact: zahin@ebryx.com
## Usage: python code1unique.py <ba_fp.csv> <reporte2Bpasted.csv>
## Dependencies: None
##*************Thank You***************##

class VTresult:
	#Declare Static Variables
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
			detec=[]
			comments=[]
			for row in file2_reader:
				md5.append(row[0])
				detec.append(row[1])
				comments.append(row[2])	

		n1= "op1analyzed.csv"
		n2= "VT_undetected.csv"
		n3= "VT_notfound.csv"
		#n4= "VT_opfile.csv"
		detfile= csv.writer(open(n1, 'a+'), delimiter=',')
		undetfile= csv.writer(open(n2, 'w'), delimiter=',')
		notfoundfile= csv.writer(open(n3, 'w'),delimiter=',')
		#optfile= csv.writer(open(n4, 'w'), delimiter=',')
		print "Initializing..."
		with open(sys.argv[1], 'rb') as f:
			try:
				file1_reader = csv.reader(f, delimiter=',')
			except IOError:
				print "Error Reading csv File", f
				sys.exit()
			index1=1 # Md5 count check
			for row in file1_reader:
				a=1
				index=0
				if ((index1%1000) == 0):
					print "Files Analyzed do far =>",index1
				if "md5sum" in row[2]:
					undetfile.writerow(row)
				else:
					for m in md5:
						if m in row[2] :	
							a+=1
							#print index1,"",m,"",detec[index],"", comments[index]
							if comments[index]== 'ML':
								#row[3]= detec[index]
								row[10]= comments[index]
								self.count_detected+=1
								detfile.writerow(row)
							elif comments[index]== 'NM':
								self.count_undetected+=1
								undetfile.writerow(row)	
							else:
								self.count_notFound+=1
								notfoundfile.writerow(row)		
							#optfile.writerow(row)
							break
						index+=1
					if a==1:
						#optfile.writerow(row)
						self.count_undetected+=1
						undetfile.writerow(row)
				index1+=1

		print "Total Detected Files :",self.count_detected
		print "Total Undetected Files :",self.count_undetected
		print "Total not Found Files :",self.count_notFound
		print "Output Files are op1analyzed.csv, VT_undetected.csv and VT_notfound.csv"
		f2.close()
		f.close()
if __name__ == '__main__':
	if len(sys.argv)!=3:
		print "     Incorrect input paramaters    "
		print "*********How to run the script*****"
		print "python code1unique.py <*.csv> <op2report2Bpasted.csv>"
		sys.exit(1)
	VT = VTresult()
	VT.main()

