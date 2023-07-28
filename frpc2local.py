#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, urllib.request


HTTPGET = urllib.request.urlopen



if __name__ == "__main__":

    ''' has root '''
    has_root = "has-root"
    DOWNURL = f"https://github.com/nblog/cloud-py3-example/blob/main/{has_root}.py?raw=true"
    exec(HTTPGET(DOWNURL).read().decode('utf-8'))

    ''' frpc '''
    frpc = "frpc"
    DOWNURL = f"https://github.com/nblog/cloud-py3-example/blob/main/{frpc}.py?raw=true"
    exec(HTTPGET(DOWNURL).read().decode('utf-8'))

    ''' frpc to local '''
    target = input("which module do you need to reverse proxy to?(default: frida-server)") or "frida-server"
    DOWNURL = f"https://github.com/nblog/cloud-py3-example/blob/main/{target}.py?raw=true"
    exec(HTTPGET(DOWNURL).read().decode('utf-8'))