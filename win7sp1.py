#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, io, sys, re, types, platform, subprocess, urllib.request

HTTPGET = urllib.request.urlopen

if not bool(os.environ.get("DEBUGPY_RUNNING")):
    source = "utils/common"
    RAW_CODE = HTTPGET(f"https://github.com/nblog/cloud-py3-example/blob/main/{source}.py?raw=true").read().decode('utf-8')

    raw_module = types.ModuleType(source.split('/')[-1])
    sys.modules[source.replace('/', '.')] = raw_module
    exec(RAW_CODE, raw_module.__dict__)

from utils.common import (
    EXTRACT,
    IS_64BIT,
)


def update_win7sp1():
    KB976932 = "https://catalog.s.download.windowsupdate.com/msdownload/update/software/svpk/2011/02/windows6.1-kb976932-x64_74865ef2562006e51d7f9333b4a8d45b7a749dab.exe"
    return


class PATCHes:

    @staticmethod
    def DOTNET():
        REBOOT = False
        if (0 == len(re.findall("Windows-7-[0-9\.]+-SP1", platform.platform()))):
            return REBOOT
        if (0 == subprocess.call( \
            "systeminfo | FIND \"KB2813430\"", shell=True, stdout=subprocess.PIPE)):
            return REBOOT

        KB2813430 = "http://download.windowsupdate.com/d/msdownload/update/software/secu/2013/05/windows6.1-kb2813430-x64_0a282a6077331c034ba2d31b85dfe65dcc71e380.msu"
        resp = HTTPGET(KB2813430)
        if (200 == resp.status):
            target = EXTRACT.bin(resp.read(), os.getcwd(), os.path.basename(resp.url))
            print(f"please install the {target}."); REBOOT = True

        return REBOOT

    @staticmethod
    def SHA2():
        REBOOT = False
        if (0 == len(re.findall("Windows-7-[0-9\.]+-SP1", platform.platform()))):
            return REBOOT
        if (0 == subprocess.call( \
            "systeminfo | FIND \"KB4474419\"", shell=True, stdout=subprocess.PIPE)):
            return REBOOT
        if (0 == subprocess.call( \
            "systeminfo | FIND \"KB4490628\"", shell=True, stdout=subprocess.PIPE)):
            return REBOOT

        KB4474419 = "http://download.windowsupdate.com/c/msdownload/update/software/secu/2019/09/windows6.1-kb4474419-v3-x64_b5614c6cea5cb4e198717789633dca16308ef79c.msu"
        resp = HTTPGET(KB4474419)
        if (200 == resp.status):
            target = EXTRACT.bin(resp.read(), os.getcwd(), os.path.basename(resp.url))
            print(f"please install the {target}."); REBOOT = True

        KB4490628 = "http://download.windowsupdate.com/c/msdownload/update/software/secu/2019/03/windows6.1-kb4490628-x64_d3de52d6987f7c8bdc2c015dca69eac96047c76e.msu"
        resp = HTTPGET(KB4490628)
        if (200 == resp.status):
            target = EXTRACT.bin(resp.read(), os.getcwd(), os.path.basename(resp.url))
            print(f"please install the {target}."); REBOOT = True

        return REBOOT


''' https://download.microsoft.com/download/C/8/7/C87AE67E-A228-48FB-8F02-B2A9A1238099/Windows6.1-KB3033929-x64.msu '''



if __name__ == "__main__":
    raise NotImplementedError("hasn't been implemented yet...")