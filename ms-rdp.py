#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, io, sys, re, types, platform, subprocess, urllib.request

HTTPGET = urllib.request.urlopen


''' ⚠ warn: will be alerted to viruses ⚠ '''
''' https://github.com/sebaxakerhtc/rdpwrap/releases/latest '''



if __name__ == "__main__":

    if 'windows' != platform.system().lower():
        raise NotImplementedError("only support windows")

    MSRDP_PORT = '3389'


    ''' reserved for frpc '''
    os.environ["FRPC_LOCAL_PORT"] = MSRDP_PORT