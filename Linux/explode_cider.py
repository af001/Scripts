#!/usr/bin/env python3

import ipaddress
import argparse

parser = argparse.ArgumentParser(description='Expand CIDR block to ip addresses')
parser.add_argument('CIDR', help='The CIDR block to expand')
parser.add_argument('-o', '--output', default='ips.txt', help='The CIDR block to expand')
args = parser.parse_args()

ips = list(ipaddress.ip_network(args.CIDR).hosts())

with open(args.output, 'w') as f:
    for ip in ips:
        f.write(str(ip) + '\n')
