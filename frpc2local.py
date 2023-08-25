#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, time, urllib.request


HTTPGET = urllib.request.urlopen



if __name__ == "__main__":

    ''' has root '''
    has_root = "has-root"
    DOWNURL = f"https://github.com/nblog/cloud-py3-example/blob/main/{has_root}.py?raw=true"
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

    ''' wait exit '''
    time.sleep(5); input("press any key to exit...")