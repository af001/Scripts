#!/usr/bin/python

import socket
import sys
import errno

def init_connection(mikrotik_ip):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((mikrotik_ip, 8291))
    s.send(starting_index)
    data = s.recv(1024)
    
    if data:
        version = data.split()

        print '[+] Mikrotik Version: %s\n' % version[-1]
        print '[+] Index File: \n', data
        print '[+] Port appears to be open!!'

request_header = ('\x12\x02')
request_footer = ('\xFF\xED\x00\x00\x00\x00')
starting_index = (request_header + 'index' + '\x00'*7 + request_footer)

print '\n[+] Winbox Port Checker\n'

if len(sys.argv) <> 2:
    print 'Usage: ' + sys.argv[0] + ' <mikrotik_ip>'
    sys.exit(0)

try:
    init_connection(sys.argv[1])
except socket.error, v:
    errorcode=v[0]
    if errorcode == errno.ECONNREFUSED:
        print '[+] Port appears to be closed :('

