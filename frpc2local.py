#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, platform, urllib.request, subprocess


HTTPGET = urllib.request.urlopen



if __name__ == "__main__":

    ''' has root '''
    has_root = "has-root.py"
    url = os.environ.get("GHPROXY","") + \
        f"https://github.com/nblog/cloud-py3-example/blob/main/{has_root}?raw=true"
    exec(HTTPGET(url).read().decode('utf-8'))

    ''' frpc '''
    frpc = "frpc.py"
    url = os.environ.get("GHPROXY","") + \
        f"https://github.com/nblog/cloud-py3-example/blob/main/{frpc}?raw=true"
    exec(HTTPGET(url).read().decode('utf-8'))

    ''' frpc to local '''
    vsremote = "vsremote.py"
    url = os.environ.get("GHPROXY","") + \
        f"https://github.com/nblog/cloud-py3-example/blob/main/{vsremote}?raw=true"
    exec(HTTPGET(url).read().decode('utf-8'))