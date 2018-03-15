#!/usr/bin/python
import ipaddress
import sys
import os

if sys.version_info[0] < 3:
 print ('Must be using Python 3')
else:


## Connection option
 while True:
    print ('')
    print (' R for Remote Forwarding  ie : forward a port from the local machine to the server machine')
    print (' L for Local Forwarding  ie : forward a port from the server machine ot the local machine')
    print ('')
    CON_OPTION = input('Choose R or L : ')
    if CON_OPTION == "R" or CON_OPTION == "L":
        if CON_OPTION == "R":
           ## Remote Server User
           USERNAME = input('Username of Remote Server for ssh Connection : ')
        else:
           ## Local System User
           USERNAME = input('Username of Local Server for ssh Connection : ')
        break


## Local port
 LOCAL_PORT = input('Local Port for Expose to Outside : ')
 while True:
    try:
      int(LOCAL_PORT)
    except ValueError:
      print ('Invalid Port number.......!')
      LOCAL_PORT = input('Local Port for Expose to Outside : ')
      continue
    else:
      break


## Remote port
 REMOTE_PORT = input('Remote Port for Pointing to Local Port : ')
 while True:
    try:
      int(REMOTE_PORT)
    except ValueError:
      print ('Invalid Port number.......!')
      REMOTE_PORT = input('Remote Port for Pointing to Local Port : ')
      continue
    else:
      break


## Remote IP Address
 REMOTE_IP = input('Remote Server IP Address : ')
 while True:
      try:
         ip = ipaddress.ip_address(REMOTE_IP)
      except ValueError:
         print ('Invalid IP Address.......!')
         REMOTE_IP = input('Remote Server IP Address : ')
         continue
      else:
         break


 data = {"CON_OPTION": CON_OPTION,
        "REMOTE_IP": REMOTE_IP,
        "LOCAL_PORT": LOCAL_PORT,
        "REMOTE_PORT": REMOTE_PORT,
        "USERNAME": USERNAME}


## Connection Establishment
 if CON_OPTION == "R":
   ## Remote Server User
   cmd = "ssh -fN -{CON_OPTION} {REMOTE_PORT}:localhost:{LOCAL_PORT} {USERNAME}@{REMOTE_IP}"
   os.system(cmd.format(**data))
 else:
   ## Local System User
   cmd = "ssh -fN -{CON_OPTION} \*:{LOCAL_PORT}:{REMOTE_IP}:{REMOTE_PORT} {USERNAME}@localhost"
   os.system(cmd.format(**data))
