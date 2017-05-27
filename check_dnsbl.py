#! /usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Script to check if the IP Address has a blacklist

Creation date: 24/01/2017
Date last updated: 19/03/2017

Nagios check_dnsbl plugin
* 
* License: GPL
* Copyright (c) 2017 DI-FCUL
* 
* Description:
* 
* This file contains the check_dnsbl plugin
* 
* Use the nrpe program to check the application are installed in remote host.
* 
* 
* This program is free software: you can redistribute it and/or modify
* it under the terms of the GNU General Public License as published by
* the Free Software Foundation, either version 3 of the License, or
* (at your option) any later version.
* 
* You should have received a copy of the GNU General Public License
* along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import os
import sys
import dns.resolver
import urllib.request
from dns import resolver
from optparse import OptionParser
from collections import OrderedDict
from itertools import repeat
import ipaddress

__author__ = "\nAuthor: Raimundo Henrique da Silva Chipongue\nE-mail: fc48807@alunos.fc.ul.pt, chipongue1@gmail.com\nInstitution: Faculty of Science of the University of Lisbon\n"
__version__= "1.0.0"

# define exit codes
ExitOK = 0
ExitWarning = 1
ExitCritical = 2
ExitUnknown = 3

def check_connectivity():
    try:
        urllib.request.urlopen('http://194.210.238.163', timeout=2)
        return True

    except urllib.request.URLError:
        return False

def open_bl(opts):
    #newitem = str(opts.blist)
    Ignore = []
    if opts.Ignore:
            Ig = [i for i in opts.Ignore.split(",")]
            Ignore.extend([i for i in Ig])
            Ignore = sorted(list(set(Ignore)))
            
    if opts.ignore:
        blacklist = []
        
    else:
        blacklist = ["zen.spamhaus.org", "spam.abuse.ch", "cbl.abuseat.org","virbl.dnsbl.bit.nl",
               "dnsbl.inps.de", "ix.dnsbl.manitu.net", "dnsbl.sorbs.net", "bl.spamcannibal.org",
               "bl.spamcop.net", "xbl.spamhaus.org", "pbl.spamhaus.org", "dnsbl-1.uceprotect.net",
               "dnsbl-2.uceprotect.net", "dnsbl-3.uceprotect.net", "db.wpbl.info", "safe.dnsbl.sorbs.net",
                "b.barracudacentral.org", "access.redhawk.org", "dnsbl.justspam.org","dnsbl.sorbs.net",
                 "noservers.dnsbl.sorbs.net","rhsbl.sorbs.net","sbl.spamhaus.org","xbl.spamhaus.org",
                 "pbl.spamhaus.org","dnsbl.cobion.com","dyna.spamrats.com"]
    
    if opts.blist:
        newitem = [i for i in opts.blist.split(",")]
        blacklist.extend([i for i in newitem])
        blacklist = sorted(list(set(blacklist) - set(Ignore)))
        return sorted(list(set(blacklist)))
    else:
        blacklist = sorted(list(set(blacklist) - set(Ignore)))
        return sorted(blacklist)
                     
def dns_f(opts):
    if check_connectivity():
        myIP = opts.host       
        if not myIP:
            myIP = (os.popen("dig +short myip.opendns.com @resolver1.opendns.com").read())
            myIP = myIP.replace("\n", "")

        blacklist = open_bl(opts)
        blacklisted = []
        noblacklisted = []
        timeout = []
        nonameserver = []
        noanswer = []
        number = 0      
        for bl in blacklist:
            try:
                my_resolver = dns.resolver.Resolver()
                query = '.'.join(reversed(str(myIP).split("."))) + "." + bl
                my_resolver.timeout = 1
                my_resolver.lifetime = 1
                answers = my_resolver.query(query, "A")        
                if answers:                                 
                    answer_txt = my_resolver.query(query, "TXT")
                    blacklisted.append(str(bl))
                    number = number + 1

            except dns.resolver.NXDOMAIN:
                noblacklisted.append(str(bl))

            except dns.resolver.Timeout:
                timeout.append(str(bl))

            except dns.resolver.NoNameservers:
                nonameserver.append(str(bl))

            except dns.resolver.NoAnswer:
                noanswer.append(str(bl))
                
        if blacklisted:
            print("IP %s LISTED in %s blacklist: %s" %(myIP, number, ', '.join(blacklisted)))
            sys.exit(ExitCritical)

        else:
            print("IP %s NOT LISTED in dns blacklist"%myIP)
            sys.exit(ExitOK)
    else:
        print("Error, check you internet connection")
        sys.exit(ExitUnknown)

def main():
    parser = OptionParser("usage: %prog -H <IP address> and -l <anylist.com,anylist.org>, black list you have to check")
    parser.add_option("-H","--hostaddress", dest="host", help="Specify the IP address you want to check")
    parser.add_option("-l","--list", dest="blist", default=False, type="string", help="If you heve an list to add, please enter -l <anylist.com,anylist.org>")
    parser.add_option("-V","--version", action="store_true", dest="version", help="This option show the current version number of the program and exit")
    parser.add_option("-A","--author", action="store_true", dest="author", help="This option show author information and exit")
    parser.add_option("-i","--ignore", action="store_true", dest="ignore",
                      help="Use this option to ignore all pre-installed blacklists")
    parser.add_option("-I","--Ignore", dest="Ignore",default=False, type=str,
                      help="Use this option to ignore one or multiple pre-installed blacklist")

    (opts, args) = parser.parse_args()
    if opts.author:
        print(__author__)
        sys.exit()
    if opts.version:
        print("check_dnsbl.py %s"%__version__)
        sys.exit()
    if opts.ignore:
        if not opts.blist:
            parser.error("When using -i option, you need to specify at least one blacklist.")
    if opts.host:
        try:
            ip = ipaddress.ip_address(opts.host)  
        except ValueError:
            parser.error("Incorrect IP Address.")
        dns_f(opts)
    else:
        dns_f(opts)
 
if __name__ == '__main__':
    main()

