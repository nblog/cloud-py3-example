#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, io, sys, re, types, platform, subprocess, urllib.request

HTTPGET = urllib.request.urlopen

if not bool(os.environ.get("DEBUGPY_RUNNING")):
    target = "utils/common"
    RAW_CODE = HTTPGET(f"https://github.com/nblog/cloud-py3-example/blob/main/{target}.py?raw=true").read().decode('utf-8')

    raw_module = types.ModuleType('common')
    sys.modules['utils.common'] = raw_module
    exec(RAW_CODE, raw_module.__dict__)


''' ⚠ warn: will be alerted to viruses ⚠ '''
''' https://github.com/sebaxakerhtc/rdpwrap/releases/latest '''



if __name__ == "__main__":

    if 'windows' != platform.system().lower():
        raise NotImplementedError("only support windows")

    MSRDP_PORT = '3389'


    os.environ["EXEC_LOCAL_PORT"] = MSRDP_PORT