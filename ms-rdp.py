#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, re, platform, urllib.request, subprocess


HTTPGET = urllib.request.urlopen



if __name__ == "__main__":

    if 'windows' != platform.system().lower():
        raise NotImplementedError("only support windows")

    MSRDP_PORT = '3389'


    ''' reserved for frpc '''
    os.environ["FRPC_LOCAL_PORT"] = MSRDP_PORT