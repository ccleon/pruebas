import glob
import os
import subprocess
import re

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
file.write("Session = "+str(session))

#variables to get only specific information.


with open(latest_file_client, 'r') as filehandle:  
	# Pillamos la primera linea que contiene la IP del cliente
	line = filehandle.readline()
	ip = line.split("=")
	file.write("IP Client =" + ip[1])

	
	for line in filehandle:
		if "Content-Base:" in line :
				ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', line)
				file.write("IP Server = "+ip[0] + "\n")
				file.write (20*'-'+"Informacion de los puertos"+20*'-'+"\r\n")

		if "Transport:" in line :
			if "client_port" and "server_port" in line :
				
				line = line.split(";")
				#line[2]= client information
				#line[3] = server information

				file.write(line[2] + " " + line [3]+"\r\n")

    	#To get audio codification information

		# if "RTP subsession 'audio" in line :
		# 	file.write (20*'-'+"codificacion del audio"+20*'-'+"\r\n")
		# 	line = line.split("/")[1].split("'")[0]
		# 	print line
		# 	file.write("Codec del audio ="+ line)		



		if "samplerate:" in line :
			file.write (20*'-'+"codificacion del audio"+20*'-'+"\r\n")
			print line 
			array=(line.split("] ")[2]).split("g: ")[1].split(" ")
			print array
			for i in array :
				if ":" not in i  :
					file.write("acodec=")
				i=i.replace(':','=')
				file.write(i)
				file.write('\n')
    			print i
    		#Close the client log file to start parsing the server side
    	


file.write (20*'-'+"codificacion del video"+20*'-'+"\r\n")
with open(latest_file_server, 'r') as filehandle:  
    for line in filehandle:
		if "source fps " in line:
			line= line.split(": ")[1].split(", ")
			file.write(line[0]+'\r\n')
			file.write(line[1])
		if "core stream output debug: usi" in line:
			line=line.split("{")[1].split(',')
			file.write(line[0]+'\n'+line[1]+'\n')

