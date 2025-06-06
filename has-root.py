#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, getpass


def has_root():
    user = getpass.getuser()

    if os.name == 'nt':
        try:
            open(f"\\\\.\\{os.getenv('SYSTEMDRIVE','C:')}").close()
            return (True, user)
        except (PermissionError, OSError):
            return (False, user)
    else:
        try:
            return (os.geteuid() == 0, user)
        except AttributeError:
            return (user == 'root', user)



if __name__ == "__main__":

    root = has_root()
    if (not root[0]):
        print( f"\n!!! warn: current {root[1]} is not root !!!\n" )

        if ("HAS_ROOT" in os.environ): exit(1)