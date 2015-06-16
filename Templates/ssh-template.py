import paramiko
import time
import re
import sys


#Open SSHv2 connection to devices
def open_ssh_conn(ip):
    #Change exception message
    try:
        #Define the Credentials file taking its name from he user in run time
        user_file = sys.argv[1]
        
        #Define the commands file aking its name from he user in run time
        cmd_file = sys.argv[2]

        #Define SSH parameters
        selected_user_file = open(user_file, 'r')
        
        #Starting from the beginning of the file
        selected_user_file.seek(0)

        username = selected_user_file.readlines()[0].split(',')[0]

                
        #Starting from the beginning of the file
        selected_user_file.seek(0)
        
        #password = selected_user_file.readlines()[0].split(',')[1]
        password = selected_user_file.readlines()[0].split(',')[1].rstrip("\n")
        
        #Logging into device
        session = paramiko.SSHClient()

        #for testing purpose only. This allows auto-accepting host keys
        #Do Not use in production. The default would be Reject Policy()
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        print "ip: " +ip 
        print "user: " +username 
        print "pword: " +password 
         
        session.connect(ip, username = username, password = password)        

        #DEBUG
        #outputoflogin = connection.recv(65535)
        #print outputoflogin

       
        connection = session.invoke_shell()	
        
        #Setting terminal length for entire output - no pagination
        connection.send("terminal length 0\n")
        time.sleep(1)
        
        #Entering global config mode
        connection.send("\n")
        connection.send("configure terminal\n")
        time.sleep(1)
        
        #Open user selected file for reading
        selected_cmd_file = open(cmd_file, 'r')
            
        #Starting from the beginning of the file
        selected_cmd_file.seek(0)

        #DEBUG
        print selected_cmd_file
        
        #Writing each line in the file to the device
        for each_line in selected_cmd_file.readlines():
            connection.send(each_line + '\n')
            time.sleep(2)
        
        #Closing the user file
        selected_user_file.close()
        
        #Closing the command file
        selected_cmd_file.close()
        
        #Checking command output for IOS syntax errors
        output = connection.recv(65535)
        
        
        if re.search(r"% Invalid input detected at", output):
            print "* There was at least one IOS syntax error on device %s" % ip
        else:
            print "\nDONE for device %s" % ip
            
        #Test for reading command output
        print output + "\n"
        
        #Closing the connection
        session.close()
     
    except paramiko.AuthenticationException:
        print "* Invalid username or password. \n* Please check the username/password file or the device configuration!"
        print "* Closing program...\n"
		
#Calling the SSH function
open_ssh_conn("192.168.2.101")
