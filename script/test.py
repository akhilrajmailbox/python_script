#!/usr/bin/python
import os
import sys
import os.path
from subprocess import Popen, PIPE
from pathlib import Path
import netifaces as ni


os.environ["TERM"] = "xterm"
SERVICE1 = ["xinetd", "apache2"]
MOD1 = ["rewrite", "cgi"]
SRC1 = '/etc/apache2/sites-available/nagios.conf'
DES1 = '/etc/apache2/sites-enabled/nagios.conf'


class bcolors:
 HEADER = '\033[95m'
 OKBLUE = '\033[94m'
 OKGREEN = '\033[92m'
 WARNING = '\033[93m'
 FAIL = '\033[91m'
 ENDC = '\033[0m'
 BOLD = '\033[1m'
 UNDERLINE = '\033[4m'



class preconfig():

 def intro(self):
  print bcolors.OKBLUE +  "-----------------------------------" + bcolors.ENDC
  print bcolors.OKGREEN + "|    optional docker variable     |" + bcolors.ENDC
  print bcolors.OKBLUE +  "-----------------------------------" + bcolors.ENDC
  print bcolors.OKBLUE +  "-----------------------------------" + bcolors.ENDC
  print bcolors.OKGREEN + "|       1)  MAIL_ADDRESS          |" + bcolors.ENDC
  print bcolors.OKBLUE +  "-----------------------------------" + bcolors.ENDC
  print bcolors.OKGREEN + "|       2)  HOST_IP               |" + bcolors.ENDC
  print bcolors.OKBLUE +  "-----------------------------------" + bcolors.ENDC
  print bcolors.OKGREEN + "|       3)  LOCAL_MONITOR         |" + bcolors.ENDC
  print bcolors.OKBLUE +  "-----------------------------------" + bcolors.ENDC
  print ""
  print bcolors.UNDERLINE + "###          MAIL_ADDRESS          ###" + bcolors.ENDC
  print ""
  print bcolors.WARNING + "You can provide mail address for getting notification from nagios server" + bcolors.ENDC
  print ""
  print ""
  print bcolors.UNDERLINE + "###          HOST_IP               ###" + bcolors.ENDC
  print ""
  print bcolors.WARNING + "You can provide the ip-address of the docker machine if you wish," + bcolors.ENDC
  print bcolors.WARNING + "so that you can connect the remote machines with nagios server by using the 'docker machine ip' and 'port no'" + bcolors.ENDC
  print ""
  print bcolors.WARNING + "If you don't provide 'HOST_IP' then It choose 'container ip' as default ip address for nrpe configuration, " + bcolors.ENDC
  print bcolors.WARNING + "so communication between 'remote machine' and 'nagios server (this container)' is not possible" + bcolors.ENDC
  print ""
  print ""
  print bcolors.UNDERLINE + "###          LOCAL_MONITOR         ###" + bcolors.ENDC
  print ""
  print bcolors.WARNING + "If you want the nagios server to monitor its own host (the container itself [localhost portion in ui]), use this environment variable, value should be 'Y'" + bcolors.ENDC
  print bcolors.WARNING + "If you don't want to monitor the the container itself, Do not use this Environment variable" + bcolors.ENDC
  print ""
  print bcolors.WARNING + "If you don't want localhost monitoring, It will shows some error because of the empty host-list," + bcolors.ENDC
  print bcolors.WARNING + "you can add new '<<name>>.cfg' file which have hosts and services under '/usr/local/nagios/etc/servers' and reload the service 'service nagios reload' or mount the location to the docker machine with the cfg file" + bcolors.ENDC
  print ""
  print ""
  print bcolors.WARNING + "Configuring........" + bcolors.ENDC
  print ""


HTPASSWORD="xc"
HOST_IP=""
bootsrap = Path("/usr/local/nagios/etc/nagios-bootsrapped")
htpasswd = Path("/usr/local/nagios/etc/htpasswd.users")
nagios_user = Path("/usr/local/bin/nagios-user")



class config():

 def bootstrap(self):
     if not bootsrap.is_file():
          print bcolors.OKGREEN + "configuring nagios" + bcolors.ENDC
          if not htpasswd.is_file():
                 if HTPASSWORD == "":
                    print bcolors.FAIL + "Please provide all environment variable while run the 'docker run command' with -e option" + bcolors.ENDC
                    print ""
                    print bcolors.OKBLUE +  "-----------------------------------" + bcolors.ENDC
                    print bcolors.OKGREEN + "|    indeeded docker variable     |" + bcolors.ENDC
                    print bcolors.OKBLUE +  "-----------------------------------" + bcolors.ENDC
                    print bcolors.OKBLUE +  "-----------------------------------" + bcolors.ENDC
                    print bcolors.OKGREEN + "|    1)  HTPASSWORD               |" + bcolors.ENDC
                    print bcolors.OKBLUE +  "-----------------------------------" + bcolors.ENDC
                    print ""
                    print bcolors.FAIL +  "USERNAME : nagiosadmin" + bcolors.ENDC
                    print bcolors.FAIL +  "PASSWORD : The password you are providing with 'HTPASSWORD' environment variable" + bcolors.ENDC
                    print ""
                    sys.exit()
                 HTPASS = Popen([ "htpasswd", "-b", "-c", "/usr/local/nagios/etc/htpasswd.users", "nagiosadmin", HTPASSWORD], stdin=PIPE, stdout=PIPE, stderr=PIPE)
                 stdout, stderr = HTPASS.communicate()
                 print "Stdout:", stdout
                 print "Stderr:", stderr


          print ""
          if HOST_IP == "":
             ni.ifaddresses('enp3s0')
             HOST_IP = ni.ifaddresses('enp3s0')[ni.AF_INET][0]['addr']
             print HOST_IP

             filename="./ba"
             f = open(filename, "a+")
             f.write("# default: on\n");
             f.write("# description: NRPE (Nagios Remote Plugin Executor)\n");
             f.write("service nrpe\n");
             f.write("{\n");
             f.write("        flags           = REUSE\n");
             f.write("        socket_type     = stream\n");
             f.write("        port            = 5666\n");
             f.write("        wait            = no\n");
             f.write("        user            = nagios\n");
             f.write("        group           = nagios\n");
             f.write("        server          = /usr/local/nagios/bin/nrpe\n");
             f.write("        server_args     = -c /usr/local/nagios/etc/nrpe.cfg --inetd\n");
             f.write("        log_on_failure  += USERID\n");
             f.write("        disable         = no\n");
             f.write("        only_from       = 127.0.0.1 HOST_IP\n");
             f.write("}");
             f.close()

          print ""
          if not nagios_user.is_file():
                 f = open(nagios-user, "a+")
                 f.write("#!/bin/bash");
                 f.write("htpasswd -b /usr/local/nagios/etc/htpasswd.users \$1 \$2");
                 f.close()


          bashCommand = "chmod 777 /usr/local/bin/nagios-user"
          os.system(bashCommand)





class postconfig():

 def servcie_start1(self):
  for SERVICES in SERVICE1:
	SER = Popen([ "service", SERVICES, "restart"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        stdout, stderr = SER.communicate()
        print "Stdout:", stdout
       	print "Stderr:", stderr

 def mod_start(self):
  for MODS in MOD1:
        MOD = Popen([ "a2enmod", MODS], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        stdout, stderr = MOD.communicate()
       	print "Stdout:", stdout
        print "Stderr:", stderr

 def symlink(self):
  os.symlink(SRC1, DES1)
  print "symlink created"

 def servcie_start2(self):
  SERVICE2 = ["xinetd", "nagios", "apache2", "postfix"]
  for SERVICES in SERVICE2:
	SER = Popen([ "service", SERVICES, "restart"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
	stdout, stderr = SER.communicate()
	print "Stdout:", stdout
	print "Stderr:", stderr

 def ownership(self):
  OWERSHIP = Popen([ "chown", "-R", "nagios:nagios", "/usr/local/nagios/etc/servers"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
  stdout, stderr = OWERSHIP.communicate()
  print "Stdout:", stdout
  print "Stderr:", stderr







#classname = first()
#classname.servcie_start1()
#classname.mod_start()


classname = config()
classname.bootstrap()

