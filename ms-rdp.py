#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, io, sys, re, pathlib, types, platform, subprocess, urllib.request

HTTPGET = urllib.request.urlopen

if not bool(os.environ.get("DEBUGPY_RUNNING")):
    source = "utils/common"
    RAW_CODE = HTTPGET(f"https://github.com/nblog/cloud-py3-example/blob/main/{source}.py?raw=true").read().decode('utf-8')

    raw_module = types.ModuleType(source.split('/')[-1])
    sys.modules[source.replace('/', '.')] = raw_module
    exec(RAW_CODE, raw_module.__dict__)

from utils.common import (
    EXTRACT, GITHUB_RELEASES
)


class rdpwrap:
    ''' ⚠ warn: will be alerted to viruses ⚠ '''
    ''' https://github.com/sebaxakerhtc/rdpwrap/releases/latest '''
    ''' https://github.com/sebaxakerhtc/rdpwrap.ini '''

    RDP_DIRECTORY = os.path.expandvars(os.path.join(r"$ProgramFiles", "RDP Wrapper"))

    def download(self, target_dir=".", tagVer="latest"):
        if not os.path.exists(self.RDP_DIRECTORY):
            os.makedirs(self.RDP_DIRECTORY, exist_ok=True)

        # add exclusion `Windows Defender`
        subprocess.run(["powershell", "-Command", 
            f"Add-MpPreference -ExclusionPath '{self.RDP_DIRECTORY}'"], 
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        downUrl = GITHUB_RELEASES(source="sebaxakerhtc/rdpwrap").geturl(f"RDPW_Installer.exe", tagVer)
        resp = HTTPGET(downUrl)
        if (200 == resp.status):
            return EXTRACT.bin(resp.read(), target_dir=self.RDP_DIRECTORY, target_name=os.path.basename(downUrl))

        raise Exception("download failed: " + downUrl)

    def run(self, argv=[], binpath=''):
        subprocess.run([binpath, *argv], cwd=self.RDP_DIRECTORY)



if __name__ == "__main__":

    if 'windows' != platform.system().lower():
        raise NotImplementedError("only support windows")

    ''' runas `administrator` '''
    os.environ.setdefault("HAS_ROOT", "1")
    DOWNURL = f"https://github.com/nblog/cloud-py3-example/blob/main/has-root.py?raw=true"
    exec(HTTPGET(DOWNURL).read().decode('utf-8'))

    # rdp = rdpwrap()
    # rdp.download(); rdp.run()

    MSRDP_PORT = '3389'
    os.environ["EXEC_LOCAL_PORT"] = MSRDP_PORT