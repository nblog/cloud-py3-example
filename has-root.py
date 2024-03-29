#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os


def has_root():
    if os.name == 'nt':
        try:
            open(f"\\\\.\\{os.environ.get('SYSTEMDRIVE','C:')}").close()
        except PermissionError:
            return (False, os.environ['USERNAME'])
        else:
            return (True, os.environ['USERNAME'])
    else:
        if os.geteuid() == 0:
            return (True, os.environ['SUDO_USER'])
        else:
            ''' https://docs.python.org/3/library/getpass.html#getpass.getuser '''
            has_name = list(filter(os.environ.get, ("LOGNAME", "USER", "LNAME", "USERNAME")))[0]
            return (False, os.environ[has_name])



if __name__ == "__main__":

    root = has_root()
    if (not root[0]):
        print( f"\n!!! warn: current {root[1]} is not root !!!\n" )

        if ("HAS_ROOT" in os.environ): exit(1)