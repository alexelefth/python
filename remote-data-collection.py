#!/usr/bin/python3

#Collect data from remote system every 10 seconds

import os
import time
import paramiko
import xml.etree.ElementTree as ET

hostname = "ip address"
myuser = "user"
mySSHK = "/home/alex/.ssh/id_rsa"

#paramiko ssh client
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) #no known hosts error
ssh.connect(hostname, username=myuser, key_filename=mySSHK)

#paramiko sftp client
sftp_client = ssh.open_sftp()

while True:
        #timestamp
        t = time.localtime()
        timestamp = str(t.tm_year).zfill(2) + '-' + str(t.tm_mon).zfill(2) + '-' + str(t.tm_mday).zfill(2) + " " + str(t.tm_hour).zfill(2) + ':' + str(t.tm_min).zfill(2) + ':' + str(t.tm_sec).zfill(2)
        #memory info
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("free -k")
        meminfo = ssh_stdout.readlines()[1].rstrip()[4:]

        #disk info
        nvme0n1p1 = -1
        nvme0n1p2 = -1
        nvme0n1p3 = -1
        sda3 = -1
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("df -H")
        df_H = ssh_stdout.readlines()

        for disk in df_H:
                if "sda3" in disk:
                        sda3 = disk.strip().split()[4][:-1]
                elif "nvme0n1p1" in disk:
                        nvme0n1p1 = disk.strip().split()[4][:-1]
                elif "nvme0n1p2" in disk:
                        nvme0n1p2 = disk.strip().split()[4][:-1]
                elif "nvme0n1p3" in disk:
                        nvme0n1p3 = disk.strip().split()[4][:-1]

        #loadavg
        f = sftp_client.open('/proc/loadavg',mode='r')
        loadavg = f.readlines()[0].rstrip()
        f.close()

        #xml like info
        f = sftp_client.open('/proc/path/to/xml_info',mode='r')
        xml_info = f.read().decode()
        tree = ET.fromstring(xml_info)
        get_xml = tree.find('.//TAG')
        get_text = get_xml.text


        #Write statistics to files
        #loadavg
        with open("/home/alex/logs/loadavg", "a") as f:
                f.write(timestamp + " " + loadavg + '\n')
                f.close()
        #meminfo
        with open("/home/alex/logs/meminfo", "a") as f:
                f.write(timestamp + meminfo + '\n')
        #disk usage
        with open("/home/alex/logs/diskfree", "a") as f:
                f.write(timestamp + " " + str(sda3) + " " + str(nvme0n1p1) + " " +  str(nvme0n1p2) + " " + str(nvme0n1p3) + "\n")
        time.sleep(10)

ssh.close()
