#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os


def has_root():
    if os.name == 'nt':
        try:
            # only windows users with admin privileges can read the C:\windows\temp
            temp = os.listdir(os.sep.join([os.environ.get('SystemRoot','C:\\windows'),'temp']))
        except:
            return (False, os.environ['USERNAME'])
        else:
            return (True, os.environ['USERNAME'])
    else:
        if 'SUDO_USER' in os.environ and os.geteuid() == 0:
            return (True, os.environ['SUDO_USER'])
        else:
            return (False, os.environ['USERNAME'])



if __name__ == "__main__":

    root = has_root()
    if (not root[0]): print( f"\n!!! warn: current {root[1]} is not root !!!\n" )
    if ("has_root_check" in os.environ and not root[0]): exit(1)