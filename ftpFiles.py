#!/usr/bin/env python

import sys
from ftplib import FTP
import json

def get(host=None,files=[],user=None,passwd=None,timeout=5.0):
    """grab files from FTP server using given specifications
    args:
        host = hostname of ftp server
        files = list of absoluate path file names
        user = (None will give anonymous login)
        passwd = (None will give anonymous@ password)
        timeout = floating point number of seconds
    returns:
        a json string of each server, file names and sizes
    """
    # can't do much without a hostname or list of files
    if(not host or not files):
        sys.exit(1)

    # initalize dictionary with filenames as keys and file size as vals
    results = dict()

    # connect to server, timeout in seconds
    try:
        ftp = FTP(host=host,user=user,passwd=passwd,timeout=timeout)
    except Exception as e:
        sys.stderr.write(str(e)+'\n')
        raise

    # login with credentials or anonymous/anonymous@ if 'None'
    try:
        ftp.login()
    except Exception as e:
        sys.stderr.write(str(e)+'\n')
        raise

    for fname in files:
        # # split absolute file name into path and name
        # filedir = '/'.join(fname.split('/')[:-1])
        # filename = fname.split('/')[-1]

        # # first CWD into the directory that contains the file
        # try:
        #     ftp.cwd(filedir)
        # except Exception as e:
        #     sys.stderr.write(str(e)+'\n')
        #     raise

        # now get the file
        data = []
        try:
            ftp.retrbinary('RETR {0}'.format(fname), data.extend)
        except Exception as e:
            sys.stderr.write(str(e)+'\n')
            raise
        finally:
            results[fname] = len(data)

    #all done, clean up
    try:
        ftp.quit()
    except Exception as e:
        sys.stderr.write(str(e)+'\n')
        raise

    #we made it, return json results
    print json.dumps(results)
    return json.dumps(results)


if __name__ == '__main__':
    servers = ['ftp.debian.org'
               'debian.cs.binghamton.edu',
               'debian.ec.as6453.net',
               'debian.gtisc.gatech.edu',
               'debian.uchicago.edu']

    files = ['/debian/README']

    results = dict()
    for server in servers:
        results[server] = get('ftp.debian.org',files)
    print results
