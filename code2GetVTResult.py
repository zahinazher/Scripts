#!/usr/bin/python
import simplejson
import urllib
import urllib2
import sys
import csv
import os
import re
import math
api_key_index = 0
API_KEY_LIST =  ['f76bdbc3755b5bafd4a18436bebf6a47d0aae6d2b4284f118077aa0dbdbd76a4'
		    ,'9c04098ab1bd2c8d2081b07d6184d4e58bf5750a5d187505cb20e7c8e2ba9a89'
		    ,'a8452a77d77474da517a686c2fff1e30b14bb8fb34fc5ea8743bcf7edcc4176b'
                    ,'371064b22215809946110c23fb8fef7ad15f8f0884d2a3daf05057105be26a09'
                    ,'4cb646513d17dacb927b8a7a0703da5a5f03c7689a6d5801377690d6c5e4d9fc'
                    ,'10700e96555cd609759b4fb6be0e2d015a294756c996e4ffc63ab43d1154b246'
                    ,'0fbaf05f297b351f1560ac1edc91374cca177f809b4bd4d0a73d68129c247ffc'
                    ,'2ccb0302267e65ebc7e006cef5a7486e12eb16ce3e61326aedf1198c6e6930f9'
                    ,'114a0a342d2bbfc26e1af24a32504271fd8fbcfada8ae7942665623c812afbbd'
                    ,'2142fb59ef62b8ec658ca3a95d05dd81cc102085cbd7d74d44b3444d8d38a582'
                    ,'171bcbc7bbf06cb5f795da7b7c65250b5a3e3d7e513d9a83702eaba4aa8b1cdd'
                    ,'9f79e26ab046dfe5f6dc9c2fec2e856d85e1e62c6e2fdaa66236d97e5c62cf51'
                    ,'3df6d22d9a38b050bf9f512ea4f7678ac2948d33703d990e5ca4ffa773624b7d'
                    ,'91704bf13173f20bc336bde0bd23a5c2e31b578d7dd9fd47aca44df5ddf2698d'
                    ,'fb22e4262af63cd27359798b186ad7a360d34c2b490df3974053d1a588a2feef'
                    ,'58340451df8f0362b7c77d5c0bf08cbdb8b06de52504dad158a5f86c07751d9d'
                    ,'3df6d22d9a38b050bf9f512ea4f7678ac2948d33703d990e5ca4ffa773624b7d']

def open_csv_write(filename):
#open CSV File to write
    try:
        new_csv = csv.writer(open(filename,"w"))
    except IOError:
        pass
    return new_csv

def hashes_report(s_hashes,report_file,error_file):
    retry = 3
    global api_key_index
    while retry:
        try:
            url = "https://www.virustotal.com/vtapi/v2/file/report"
            parameters = {"resource": s_hashes, 
            "apikey": API_KEY_LIST[api_key_index]}
            data = urllib.urlencode(parameters)
            req = urllib2.Request(url, data)
            response = urllib2.urlopen(req)
            json = response.read()
            if len(json) < 80:
                print "Json error response"
                print json
                raise
            retry = 0
            f = open (report_file,'w+')
            f.write(json)
            f.seek(0)
            #results is a string of scans of all hashes
            f_results= f.read()
            f.close()
            return f_results
        except Exception as err:
            retry = retry - 1
            print err
            if retry == 0:
                s_hashes_temp = s_hashes.replace(',', '\n')
                #error_file.write("md5s")   # put in quotes by ZHN
                #error_file.write('\n')
                #error_file.flush()       
            api_key_index  = api_key_index +1
            if api_key_index == len(API_KEY_LIST):
                api_key_index = 0
            
    return ""
def rm_invalid_text(f_results):
    invalid_text = re.findall(r'\s*\{("response_code.*?)"\}', f_results)
    results= f_results
    i=0
    while i<len(invalid_text):
        results= results.replace(invalid_text[i],'')
        i+=1
    return results, invalid_text

def extract_invalid_hashes(invalid_text):    
    invalid_text= ','.join(invalid_text)
    invalid_md5s = re.findall(r'\s"resource":\s"(.*?)",\s', invalid_text)
    return invalid_md5s

def extract_data(results):
#result is a list of scans of all hashes. i.e.[scan1,scan2,.....]
#where scan1 is a string '.....................'
    result= results.split('{"scans": {')
#split_result is a list of list of all hashes. i.e. [scan1,scan2,.....]
#where scan1 is a list =['...','...',....]
    split_result=['NULL']
    matches=['Matches']
    scan_date=['Scan_Date_Time']
    comments= ['CVE-detail']
    v_md5s = re.findall(r'\s"resource":\s"(.*?)",\s', results)
    v_md5s.insert(0,'md5_sum')
    count=1
    while count<len(result):
        detected= re.search(' "positives": (\d+)', result[count])
        matches.append(detected.group(1))
        #final.write(detected.group(1) + ', ')
        s_d= re.search(' "scan_date": "(\d+-\d+-\d+ \d+:\d+:\d+)"', result[count])
        scan_date.append(s_d.group(1))
        #final.write(scan_date.group(1) + ', ')
        split_result.append(result[count].split('}, '))
        #-------------------------Filters------------------------------------
        flag=0
        rees= re.search(r'SuperScan',result[count],re.IGNORECASE)
        if rees:
            comments.append(rees.group(0)+';not a virus')
            flag=1
        rees= re.search(r'DNAScan',result[count],re.IGNORECASE)
        if flag==0:    
            if rees:
                comments.append('DNAScan; not a virus')
                flag=1
        rees= re.search(r'joke',result[count],re.IGNORECASE)
        if flag==0:    
            if rees:
                comments.append('joke; not a virus')
                flag=1
        rees= re.search(r'not.a.virus',result[count],re.IGNORECASE)
        if flag==0:    
            if rees:
                comments.append('not a virus')
                flag=1
    #---------------------Adware in satistics has been counted as 'adware,'
    #so care must be taken while calculating stats; may be the string is to be modified to be modified
        rees= re.findall(r'ad[wi]',result[count],re.IGNORECASE)
        if flag==0:    
            if rees:
                per= (len(rees)*100)/int(detected.group(1))
                if per>=20:
                    comments.append('adware: ' + str(len(rees))+ '::' + str(per) + '%')
                else:
                    comments.append('adware detail analysis required: ' + str(len(rees))+ '::' + str(per) + '%')
                flag=1
        rees= re.search(r'hacktool',result[count],re.IGNORECASE)
        if flag==0:    
            if rees:
                comments.append('Hack Tool;not a virus')
                flag=1
        rees= re.search(r'DNS(.*?)Changer',result[count],re.IGNORECASE)
        if flag==0:    
            if rees:
                comments.append('DNSChanger;not a virus')
                flag=1
        rees= re.search(r'PC(.*?)Client',result[count],re.IGNORECASE)
        if flag==0:    
            if rees:
                comments.append('PC_Client;not a virus')
                flag=1
        
        if flag==0:    
            comments.append('')
        count+=1


    #In split_result[] the last two elements/strings are useless    
    list_of_strues=['AV:Results']
    list_of_sresults=['Results']
    list_of_sAVs=['AVs']
    trues=[]
    results_only=[]
    AV_only=[]
    # count is for complete scan of one hash
    count=1
    # split_count is for details of one hash
    split_count=0
    
    while count<len(result):
        while split_count<len(split_result[count]):
            res= re.findall(r'"(.*?)":.*?true.*?"result":\s"(.*?)"',split_result[count][split_count])
            if res!=[]:
                trues.append( res[0][0]+':'+res[0][1])
                results_only.append(res[0][1])
                AV_only.append(res[0][0])
            split_count+=1
        split_count=0
        s_trues=';'.join(trues)
        s_res=';'.join(results_only)
        s_AV=';'.join(AV_only)
        list_of_strues.append(s_trues)
        list_of_sresults.append(s_res)
        list_of_sAVs.append(s_AV)
        trues=[]
        results_only=[]
        AV_only=[]
        count+=1
    
    return v_md5s,scan_date,matches,comments,list_of_strues,list_of_sresults,list_of_sAVs


def write_data(csv_writer, results, invalid_text):
    (v_md5s,scan_date,matches,comments,list_of_strues,list_of_sresults,list_of_sAVs)= extract_data(results)
    invalid_md5s= extract_invalid_hashes(invalid_text)
    count=1

    
    while count<len(v_md5s):
	comment = 'NM'
	if int(matches[count]) >= 5:
		comment='ML'
	
	cve_info = []
	cve = list_of_sresults[count]
	cve1 = re.findall(r'CVE.*?;',cve)

	for result in cve1:
		if (re.search(r'CVE.*;',str(result))):
			cve = re.search(r'CVE.*',str(result)).group()
			#print cve
			cve_info.append(cve)
	if len(cve_info)==0:
		cve_result = 'NA'
	else:
		cve_result = cve_info[0]
	#print cve_info[0]

        csv_writer.writerow((v_md5s[count],matches[count],comment,cve_result,list_of_strues[count],list_of_sresults[count],list_of_sAVs[count]))
        count+=1
    count=0
    while count<len(invalid_md5s):
        csv_writer.writerow((invalid_md5s[count],'NA','NF','NA','NA'))
        count+=1
def main():

  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.
 # args = sys.argv[1:]
  if len(sys.argv) != 2:
    print "     Incorrect input paramaters    "
    print "*********How to run the script*****"
    print "python code2GetVTResult.py <*.csv>"
    sys.exit(1)
  else:
    #args = sys.argv[1:]
    read_filename= sys.argv[1]
    with open(sys.argv[1], 'rb') as f:
 	try:
		urlAll5_reader = csv.reader(f, delimiter=',')
	except IOError:
		print "Error Reading csv File", f
		sys.exit()
	hashes = []
	for row in urlAll5_reader:
		hashes.append(row[2]);
    while '' in hashes:
	hashes.remove('')

    write_csv_filename= 'op2report2Bpasted.csv'
    error_text_file= 'err.txt'
    report_text_file= './temp_vt_results.txt'
    
    #f= open(read_filename)
    #error_file = open(error_text_file, 'w')
    #text=f.read()
    #text= text.replace('\n',',')
    #text= text.replace('\r',',')
    #hashes= text.split(',')
    #hashes= hashes[:-1]
    
    csv_writer= open_csv_write(write_csv_filename)
    #csv_writer.writerow(("md5sum","matches","Mycomments","comments","AV_Results","Results_Only","AV_Names"))
    print "Total Files : ",len(hashes)
    lengthmd5s=len(hashes)
    divisions= math.ceil(len(hashes)/float(150))
    count = 1
    index= 0
    print "divisions = ", int(divisions)
    while count < divisions:
        print '---------------------'+ str (count)+'-----------------'
        s_hashes= ','.join(hashes[index:index+150])
        f_results= hashes_report(s_hashes,report_text_file,error_file)
        (results, invalid_text)=rm_invalid_text(f_results)
        write_data(csv_writer, results, invalid_text)
        index+=150
        count+=1
	if index<lengthmd5s-2:
		print "files submitted so far = ", index
	else:
		print "files submitted so far = ", lengthmd5s
    print '---------------------'+ str (count)+'-----------------'
    s_hashes= ','.join(hashes[index:])
    f_results= hashes_report(s_hashes,report_text_file,error_file)
    (results, invalid_text)=rm_invalid_text(f_results)
    write_data(csv_writer, results, invalid_text)


    print 'Results are written to '+ write_csv_filename + ' successfully'

if __name__ == '__main__':
  main()
