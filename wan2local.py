#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, time, urllib.request


HTTPGET = urllib.request.urlopen



if __name__ == "__main__":

    ''' local '''
    TARGET_EXEC = os.getenv("TARGET_EXEC") \
        or input("which program to switch to(default: frida-server):") or "frida-server"
    DOWNURL = f"https://github.com/nblog/cloud-py3-example/blob/main/{TARGET_EXEC}.py?raw=true"
    exec(HTTPGET(DOWNURL).read().decode('utf-8'))

    ''' wan '''
    TARGET_WAN = os.getenv("TARGET_WAN", "frpc")
    DOWNURL = f"https://github.com/nblog/cloud-py3-example/blob/main/{TARGET_WAN}.py?raw=true"
    exec(HTTPGET(DOWNURL).read().decode('utf-8'))

    input() # wait exit