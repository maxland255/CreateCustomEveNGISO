#! /usr/bin/python
print("*********************************************************************")
print("Cisco IOU License Generator - Kal 2011, python port of 2006 C version")
print("Modified to work with python3 by c_d 2014")
print("Modified to save iourc file in /opt/unetlab/addons/iol/bin/ by Maxland255 2024")
import os
import socket
import hashlib
import struct

# get the host id and host name to calculate the hostkey
hostid=os.popen("hostid").read().strip()
hostname = socket.gethostname()
ioukey=int(hostid,16)
for x in hostname:
 ioukey = ioukey + ord(x)
print("hostid=" + hostid +", hostname="+ hostname + ", ioukey=" + hex(ioukey)[2:])

# create the license using md5sum
iouPad1 = b'\x4B\x58\x21\x81\x56\x7B\x0D\xF3\x21\x43\x9B\x7E\xAC\x1D\xE6\x8A'
iouPad2 = b'\x80' + 39*b'\0'
md5input=iouPad1 + iouPad2 + struct.pack('!i', ioukey) + iouPad1
iouLicense=hashlib.md5(md5input).hexdigest()[:16]

print("IOU License: "+ iouLicense)
print(" echo '127.0.0.127 xml.cisco.com' >> /etc/hosts\n")

open("/opt/unetlab/addons/iol/bin/iourc", mode="w", encoding="utf-8").write("[license]\n" + hostname + " = " + iouLicense + ";\n")
