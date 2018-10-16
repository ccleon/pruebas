import glob
import os
import subprocess
import re

list_of_files_server = glob.glob('/home/bayes/Repositories/pruebas/logs/server*') # * means all if need specific format then *.csv
list_of_files_client = glob.glob('/home/bayes/Repositories/pruebas/logs/client*')
latest_file_server = max(list_of_files_server, key=os.path.getctime)
latest_file_client = max(list_of_files_client, key=os.path.getctime)
id_logFile = re.findall(r'\d+', latest_file_client)[0]

print latest_file_server


def fileExists():
	fn = "/home/bayes/Repositories/pruebas/infoSession/infosession"+id_logFile+".log"
	try:
	    file = open(fn, 'a')
	except IOError:
	    file = open(fn, 'w')
	return file  
 
file = fileExists()
session = subprocess.check_output('grep -m1 "Session*" '+latest_file_client+' | cut -d " " -f4 | cut -d ";" -f1', shell=True).rstrip('\n')
ip_client = ip_server = client_port = server_port = ports = "NotApplicable"
with open(latest_file_client, 'r') as filehandle:  
	channels = samplerate = bitrate = acodec = "NotApplicable" # Generamos estas variables aunque el audio no se reproduzca

	# IP CLIENT
	line = filehandle.readline()
	ip = line.split("=  ")
	ip_client = ip[1].rstrip('\n')

	for line in filehandle:
		if "Content-Base:" in line : # IP SERVER
			ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', line)
			ip_server = ip[0]
			#file.write(date)
		#if "Date" in line:
			#date = "Quitar el dia de la semana" + line.split(": ")[1]
		if "Transport:" in line : # PORTS
			if "client_port" and "server_port" in line :
				line = line.split(";")
				ports = line[2] + ", " + line [3]

		# AUDIO INFO
		if "samplerate:" in line :
			audioInfo = (line.split("] ")[2]).split("g: ")[1].split(" ")
			audioInfo[3] = audioInfo[3].rstrip('\n')
			aux = 1
			for i in audioInfo :
				if ":" in i :
					audioInfo [aux] = i.split(":")[1]
					aux += 1
			acodec = audioInfo[0]
			channels = audioInfo[1]
			samplerate = audioInfo[2]
			bitrate = audioInfo[3]
file.write("Session=" + session + ", IPClient=" + ip_client + ", IPServer=" + ip_server + ", " + ports + ", ")
file.write("AUDIO: " + "acodec="+acodec+ ", channels="+channels+ ", samplerate="+samplerate+ ", bitrate="+bitrate+ ", ")		

#### SERVER SIDE ####
with open(latest_file_server, 'r') as filehandle:  
	fps_src = fps_dst = vcodec = scale = "NotApplicable" # Generamos estas variables aunque el video no se reproduzca
	for line in filehandle:
		if "source fps" in line:
			print line
			line = line.split(": ")[1].split(", ")
			fps_src = line[0].split("=")[1]
			fps_dst = line[1].split("=")[1] # TODO: Hay que hacer un if index NOT out of range
			# TODO: entra en el if porque hay una línea que es "stream_out_transcode stream out debug: source fps 25/1, destination 25/1"
			# cual es la linea que estamos buscando?
		if "core stream output debug: usi" in line:
			videoParams=line.split("{")[1].split(',')
			vcodec = videoParams[0].split("=")[1]
			scale = videoParams[1].split("=")[1]

file.write ("VIDEO: " + "fps_src="+fps_src+ ", fps_dst="+fps_dst+ ", vcodec="+vcodec+ ", scale="+scale+ "\n")

# NOTA: El ultimo parametro que se anada al fichero de este log, debe tener un salto de linea. Si no, el filebeat no lo coge.
