#!/usr/bin/env python
#Python script to update certificates signed by LetsEncrypt with certbot and update / create them into Stored certificates inside FortiGate
# Created by ALX on 24/11/2021

import sys
import subprocess 
import shlex
import datetime
import paramiko

def sshmethod(ip,username,password, commands):
    try:
        client.connect(ip, username=username, password=password)
    except:
        print("[!] Cannot connect to the SSH Server")
        exit()
    # execute the commands
    output=[]
    for command in commands:
        #print("="*50,"command: ", command, "in", ip, "="*50)
        stdin, stdout, stderr = client.exec_command(command)
        reply = stdout.read().decode()
        #print(reply)
        err = stderr.read().decode()
        output.append(reply)
        if err:
            print(err)
            return err
    return output
		

def updatefg(dom, forti):
	folder="/etc/letsencrypt/live/" + dom
	try:
		with open(folder + "/privkey.pem") as file:
			private = file.read()
		#print(private)
		with open(folder + "/cert.pem") as file:
			cert = file.read()
		#print(cert)
	except:
		status="error"
	else:
		#workaround to force variables inside the commands (something that was not working as a nomral array
		__template__='''
		config vpn certificate local
		edit {dom}
		set private-key "{private}"
		set certificate "{cert}"
		end
		'''
		
		commands=[__template__.format(dom=dom,private=private,cert=cert)]
		
		print(commands)
		
		reply=sshmethod(forti[0], forti[1], forti[2],commands)
		status=reply
	return status

#Domains that need to be renewed (the same name will be created as the certificate name inside the fortigate)
doms=["web.domain.com",
	"vpn.domain.com"
	]
	
#Retrieve credentials from text file (to dont have them into the code)
passfile="/home/scripts/ssl_renew/credentials"
password=str(list(open(passfile))[0]).strip()

#Fortigate Credentials
forti=["fortigate_ip",
	"fortigate_user",
	"fortigate_password"
	]

#SSH METHOD DEFINITION
# initialize the SSH client
client = paramiko.SSHClient()
# add to known hosts
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

cmd = 'certbot renew'
proc = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE)
out, err = proc.communicate()
#print(out)

for dom in doms:
	status=str(out).split(dom)[1].split("\\n")[2]
	print(dom + " -> " + status)
	config="/etc/letsencrypt/renewal/" + dom + ".conf"
	if "Certificate not yet due for renewal" not in status:
		status=updatefg(dom, forti)
		print(status)
