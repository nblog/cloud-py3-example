#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, time, urllib.request


HTTPGET = urllib.request.urlopen



if __name__ == "__main__":

    ''' to execute, runas `administrator` '''
    os.environ.setdefault("HAS_ROOT", "1")
    DOWNURL = f"https://github.com/nblog/cloud-py3-example/blob/main/has-root.py?raw=true"
    exec(HTTPGET(DOWNURL).read().decode('utf-8'))

    ''' local '''
    TARGET_EXEC = os.environ.get("TARGET_EXEC") \
        or input("which program to switch to(default: frida-server):") or "frida-server"
    DOWNURL = f"https://github.com/nblog/cloud-py3-example/blob/main/{TARGET_EXEC}.py?raw=true"
    exec(HTTPGET(DOWNURL).read().decode('utf-8'))

    ''' frpc '''
    frpc = "frpc"
    DOWNURL = f"https://github.com/nblog/cloud-py3-example/blob/main/{frpc}.py?raw=true"
    exec(HTTPGET(DOWNURL).read().decode('utf-8'))

    input() # wait exit