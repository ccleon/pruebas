import glob
import os
import subprocess


def  fileExists():
	fn = "infosession.txt"
	try:
	    file = open(fn, 'a')
	    #Create a line to separate the dissimilar sessions
	    file.write(100*"-"+'\r\n')
	except IOError:
	    file = open(fn, 'w')
	return file   


list_of_files_server = glob.glob('/home/bayes/Repositories/pruebas/logs/server*') # * means all if need specific format then *.csv
list_of_files_client = glob.glob('/home/bayes/Repositories/pruebas/logs/client*')
latest_file_server = max(list_of_files_server, key=os.path.getctime)
latest_file_client = max(list_of_files_client, key=os.path.getctime)

print latest_file_client
print latest_file_server

# Open the file that contains all information about sessions.
file = fileExists()



session=subprocess.check_output('grep -m1 "Session*" '+latest_file_client+' | cut -d " " -f4 | cut -d ";" -f1', shell=True)
#print session

file.write(" Session = "+str(session))



#variables to get only specific information.
read = False
# counter and numberlines I want to read.
counter = 0
numberLines=30

with open(latest_file_client, 'r') as filehandle:  
    for line in filehandle:

    	

    	#if to get only the number of lines specified in the variable after the DESCRIBE response

    	if read :
    		counter += 1
    		#print contador
    		#print(line)

    		#if to get the date of the streaming session
    		if "Date" in line:
    			file.write(" Date = "+ line.split(": ")[1])

    		if counter > numberLines :
    			read = False


    	if "DESCRIBE response" in line :
    		read = True
        	#print(line)