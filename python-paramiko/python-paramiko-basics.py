#!/usr/local/bin/python
#
'''
This is start of a string that is unassigned and so can be used as a block comment
Assumptions: we are on a ubuntu machine 16.04 or 18.04. If the latter, we need to install
apt install -y python-minimal to get python 2.7.
We also need the following:
    sudo apt-get update
    sudo apt-get install -y python-pip
    sudo apt-get install -y python-dev
    pip install -U pip setuptools
    sudo pip install paramiko
'''

import os, re, socket
#import time
import json, subprocess, paramiko

scriptPath = os.path.dirname(os.path.realpath(__file__))
curUser = os.getenv('USER')
if curUser == 'root':
    localHome = '/root'
else:
    localHome = '/home/' + curUser

print "reading env vars "
target_hostname = os.getenv('TARGET_HOSTNAME')
target_ip = os.getenv('TARGET_IP')
user_on_target_vm = os.getenv('USER_ON_TARGET_VM')
user_password_on_target_vm = os.getenv('USER_PASSWORD_ON_TARGET_VM')
target_cloud = os.getenv('TARGET_CLOUD')
target_private_ip = os.getenv('TARGET_PRIVATE_IP')
target_vm_arch = os.getenv('ARCH', 'amd64')

print "User on Target VM: %s" % (user_on_target_vm)

# To create a 'hosts' file for use by ansible, the following works
mainServerIP = target_ip
hosts = "[master]\n" + mainServerIP + "\n[proxy]\n" + mainServerIP + "\n[worker]\n" + mainServerIP + "\n"
f = open('hosts', 'w')
f.write(hosts)
f.close()

mainServerUsername = user_on_target_vm
mainServerPassword = user_password_on_target_vm
if mainServerUsername == 'root':
    remoteHome = '/root'
    remoteApp1Dir = '/root/App1'
    remoteApp2Dir = '/root/App2'
else:
    remoteHome = '/home/' + mainServerUsername
    remoteApp1Dir = '/home/' + mainServerUsername + '/App1'
    remoteApp2Dir = '/home/' + mainServerUsername + '/App2'

print 'IP: ' + mainServerIP  + ' User: ' + mainServerUsername

# set a variable for Paramiko's ssh client
sshmainServer = paramiko.SSHClient()

# Functions to open and close the ssh connection
def sshOpenConn(ipAddress, username, password):
    sshmainServer.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    sshmainServer.load_system_host_keys()
    sshmainServer.connect(ipAddress, username=username, password=password)
    print "Connected to server " + ipAddress + "\n"

def sshCloseConn():
    sshmainServer.close()

# Function to execute a command
# Note the use of command.replace to mask sensitive info in the log,
# and the use of optional input param to the function
def sshExecCmd(command, stringToMask='N!o!n!e!'):
    print "Executing command ...... %s " % command.replace(stringToMask, "xxxxxxxxx")
    ssh_stdin, ssh_stdout, ssh_stderr = sshmainServer.exec_command(command)
    stderr = ssh_stderr.read()
    stdout = ssh_stdout.read()
    exitCode = ssh_stdout.channel.recv_exit_status()
    print ("stderr: \n{}\n ", stderr)
    print ("stdout: \n{}\n ".format(stdout))
    print "Exit status of command %s is : %d" % (command.replace(stringToMask, "xxxxxxxxx"), exitCode)
    return(stderr, stdout, exitCode)

# function to copy file(s)
def copyFiles(ipAddress, username, password):
    # create rsa keys if not already present
    sftp = sshmainServer.open_sftp()
    try:
        sftp.chdir(remoteHome + '/.ssh')  # Test if remote_path exists
    except IOError:
        sftp.mkdir(remoteHome + '/.ssh')
    sftp.put(scriptPath + '/ssh_key', remoteHome + '/.ssh/app2_id_rsa')
    sftp.put(scriptPath + '/ssh_key.pub', remoteHome + '/.ssh/app2_id_rsa.pub')
    # copy over files for App2-install to target
    sftp.put(scriptPath + '/ssh_key', remoteApp2Dir + '/ssh_key')
    sftp.put(scriptPath + '/app2_install.sh', remoteApp2Dir + '/app2_install.sh')
    sftp.put(scriptPath + '/app2_uninstall.sh', remoteApp2Dir + '/app2_uninstall.sh')
    sftp.put(scriptPath + '/hosts', remoteApp2Dir + '/hosts')
    sftp.put(scriptPath + '/checkApp2Status.sh', remoteApp2Dir + '/checkApp2Status.sh')

    # copy over files for App1-install to target
    sftp.put(scriptPath + '/app1_openLdap_config.env', remoteApp1Dir + '/app1_openLdap_config.env')
    sftp.put(scriptPath + '/installApp1FromTarball.sh', remoteApp1Dir + '/installApp1FromTarball.sh')
    sftp.close()
    print "Successfully copied keys and all the validation scripts to the mainServer \n"

def makeDirectory(dirName):
    commandToExecute = "mkdir -p " + dirName + "; rm -rf " + dirName + "/*.sh"
    stderr, stdout, exitCode = sshExecCmd(commandToExecute)
    if exitCode != 0:
        print "Failed to create directory : " + commandToExecute
        exit(1)

##### Variables have been read from environment, functions are defined, work can begin #####

# Login to mainServer and copy over id files and script files ...
# Establish the connection with server
sshOpenConn(mainServerIP, mainServerUsername, mainServerPassword)
#Update /etc/sudoers.d/ directory for non-root user, so that password will not prompted for sudo commands
if mainServerUsername != "root":
    commandToExecute = 'sudo echo "' + mainServerUsername + ' ALL=(ALL)       NOPASSWD: ALL" | cat > a ; sudo cp a /etc/sudoers.d/a'
    stderr, stdout, exitCode = sshExecCmd(commandToExecute)
    if exitCode != 0:
        print "Failed to execute command : "+ commandToExecute
        exit(1)

#create remoteApp1Dir and remoteApp2Dir
makeDirectory(remoteApp1Dir)
makeDirectory(remoteApp2Dir)

#Copy ssh keys and scripts to ssh-connected server from local
copyFiles(mainServerIP, mainServerUsername, mainServerPassword)

#Change permission of ssh keys
commandToExecute = "cd " + remoteHome + "; chmod 600 .ssh/app2_id_rsa; chmod 644 .ssh/app2_id_rsa.pub;  if [ -f .ssh/known_hosts ] ; then chmod 644 .ssh/known_hosts; fi"
stderr, stdout, exitCode = sshExecCmd(commandToExecute)
if exitCode != 0:
    print "Failed to change permission of ssh key : " + commandToExecute
    exit(1)

# chmod 755 for all files under remoteApp1Dir
commandToExecute = "sudo chmod -R 755 " + remoteApp1Dir
stderr, stdout, exitCode = sshExecCmd(commandToExecute)
if exitCode != 0:
    print "Failed to execute command : "+ commandToExecute
    exit(1)

# chmod 755 for all files under remoteApp2Dir
commandToExecute = "sudo chmod -R 755 " + remoteApp2Dir
stderr, stdout, exitCode = sshExecCmd(commandToExecute)
if exitCode != 0:
    print "Failed to execute command : "+ commandToExecute
    exit(1)

# Add github.com rsa key to known_hosts, if you need to clone from github
commandToExecute = "cd " + remoteHome + "; ssh-keyscan -t rsa github.com >> .ssh/known_hosts"
stderr, stdout, exitCode = sshExecCmd(commandToExecute)
if exitCode != 0:
    print "Failed to copy gihub.ibm.com rsa key to known_hosts : " + commandToExecute
    exit(1)

if app2_install == "true":
    app2_install_arg = os.getenv('app2_install_ARG')
    # Add target's own ssh public key to known_hosts
    commandToExecute = "cd " + remoteHome + "; cat .ssh/app2_id_rsa.pub >> .ssh/known_hosts"
    stderr, stdout, exitCode = sshExecCmd(commandToExecute)
    if exitCode != 0:
        print "Failed to copy .ssh/app2_id_rsa.pub key into known_hosts : " + commandToExecute
        exit(1)

    commandToExecute = "cd " + remoteHome + "; cat .ssh/app2_id_rsa.pub >> .ssh/authorized_keys"
    stderr, stdout, exitCode = sshExecCmd(commandToExecute)
    if exitCode != 0:
        print "Failed to copy .ssh/app2_id_rsa.pub key into authorized_keys : " + commandToExecute
        exit(1)

    # Run app2_uninstall.sh if icp installed already
    commandToExecute = "cd " + remoteHome + "/App2; ./icp_uninstall.sh " + target_vm_arch + " | tee app2_uninstall.out"
    stderr, stdout, exitCode = sshExecCmd(commandToExecute)
    if exitCode == 2:
        print "App2 NOT Installed,  no need to Uninstall"
    elif exitCode == 0:
        print "App2 Uninstalled successfully"
    else:
        print "Failed to run command: " + commandToExecute
        exit(1)
    print "App2 uninstalled successfully"
    # Run app2_provision.sh
    argsApp2Provision = " " + target_ip  + " " + user_password_on_target_vm  + " "
    commandToExecute = "cd " + remoteHome + "/App2; ./app2_provision.sh " + argsApp2Provision + " | tee app2_install.out"
    stderr, stdout, exitCode = sshExecCmd(commandToExecute)
    if exitCode != 0:
        print "Failed to run command: " + commandToExecute
        exit(1)

##### similarly for App1 installation ####
