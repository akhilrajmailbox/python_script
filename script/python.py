#!/usr/bin/env python3
import ipaddress
import sys
import os


if sys.version_info[0] < 3:
 print ('Must be using Python 3')
else:


## static Environment Variables
 REMOTE_IP = '192.168.0.100'
 REMOTE_PORT = '0'
 DIRECTORY = '/savedir/'
 USERNAME = 'remote_username'


## Provider-Local port assigning
 def provider_portassign():
   print ('')
   global LOCAL_PORT
   LOCAL_PORT = input('Which Port is being Provided ? : ')
   while True:
      try:
        int(LOCAL_PORT)
      except ValueError:
        print ('')
        print ('Invalid Port number.......!')
        LOCAL_PORT = input('Which Port is being Provided ? : ')
        continue
      else:
        break


## Provider-Saving Dynamic ports of remote server and Private Key
 def provider_portsave():
   provider_portassign()
   if not os.path.exists(DIRECTORY):
        os.makedirs(DIRECTORY)


## Consumer-Remote port consuming
 def consumer_portconsume():
   print ('')
   global REMOTE_PORT
   REMOTE_PORT = input('Which Port is being Consumed ? : ')
   while True:
      try:
        int(REMOTE_PORT)
      except ValueError:
        print ('Invalid Port number.......!')
        REMOTE_PORT = input('Which Port is being Consumed ? : ')
        continue
      else:
        break


## Consumer-Local port assigning
 def consumer_portassign():
   consumer_portconsume()

   print ('')
   global LOCAL_PORT
   LOCAL_PORT = input('Which Port is being Exposed ? : ')
   while True:
      try:
        int(LOCAL_PORT)
      except ValueError:
        print ('Invalid Port number.......!')
        LOCAL_PORT = input('Which Port is being Exposed ? : ')
        continue
      else:
        break



## Connection option
 while True:
    print ('')
    print (' Am I in provider(P) node or Consumer(C) node ?')
    print (' Choose P or C')
    print ('')
    CON_OPTION = input('Choose P or C : ')
    if CON_OPTION == "P" or CON_OPTION == "C":
        if CON_OPTION == "P":
           provider_portsave()

        elif CON_OPTION == "C":
           print ('')
           ## Local System User
           USERNAME = input('Username of Local Server for ssh Connection ?: ')
           consumer_portassign()

        break


 data = {"REMOTE_IP": REMOTE_IP,
        "LOCAL_PORT": LOCAL_PORT,
        "REMOTE_PORT": REMOTE_PORT,
        "DIRECTORY": DIRECTORY,
        "USERNAME": USERNAME}


## Connection Establishment
 if CON_OPTION == "P":
   ## Remote Server User
   print ('')
   print ('You can find the Server port details at : ' + DIRECTORY)
   cmd = "ssh -fN -R {REMOTE_PORT}:localhost:{LOCAL_PORT} {USERNAME}@{REMOTE_IP} 2> {DIRECTORY}/{LOCAL_PORT}.txt"
   os.system(cmd.format(**data))
 elif CON_OPTION == "C":
   ## Local System User
   cmd = "ssh -fN -L \*:{LOCAL_PORT}:{REMOTE_IP}:{REMOTE_PORT} {USERNAME}@localhost"
   os.system(cmd.format(**data))
