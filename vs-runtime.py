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
    IS_ARM64, IS_64BIT,
)


class dotnet:

    class TARGET:
        class dotnetunknown:
            minver = 0; name = "unknown/too low"
        class dotnet45:
            minver = 378389; name = "4.5"
        class dotnet451:
            minver = 378675; name = "4.5.1"
        class dotnet452:
            minver = 379893; name = "4.5.2"
        class dotnet46:
            minver = 393295; name = "4.6"
        class dotnet461:
            minver = 394254; name = "4.6.1"
        class dotnet462:
            minver = 394802; name = "4.6.2"
        class dotnet47:
            minver = 460798; name = "4.7"
        class dotnet471:
            minver = 461308; name = "4.7.1"
        class dotnet472:
            minver = 461808; name = "4.7.2"
        class dotnet48:
            minver = 528040; name = "4.8"
        class dotnet481:
            minver = 533320; name = "4.8.1"

        dotnetver = dotnet48

    def download(self, dotnetver=TARGET.dotnet48):
        ''' https://dotnet.microsoft.com/download/dotnet-framework '''
        dotnet = dotnetver.name.replace(".", "")

        downUrl = f"https://dotnet.microsoft.com/download/dotnet-framework/thank-you/net{dotnet}-offline-installer"
        resp = HTTPGET(downUrl)
        if (200 == resp.status):
            downUrl = re.findall("href=\"(.*?)\" onclick=", resp.read().decode("utf-8"))[0]
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                target = os.path.basename(resp.url)
                open(target, "wb").write(resp.read())

                return self.wininstall(target)

        raise Exception("download failed: " + downUrl)

    def wininstall(self, target, silent=False):
        # requires elevation
        return 0 == \
            subprocess.call(
            [target] + (["/q", "/norestart"] if(silent) else ["/passive", "/promptrestart"]))

    def version(self):
        ''' https://learn.microsoft.com/dotnet/framework/migration-guide/how-to-determine-which-versions-are-installed#minimum-version '''
        import winreg
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\NET Framework Setup\NDP\v4\Full")
            value = winreg.QueryValueEx(key, "Release")[0]
            if (value >= dotnet.TARGET.dotnet481.minver):
                return dotnet.TARGET.dotnet481
            if (value >= dotnet.TARGET.dotnet48.minver):
                return dotnet.TARGET.dotnet48
            if (value >= dotnet.TARGET.dotnet472.minver):
                return dotnet.TARGET.dotnet472
            if (value >= dotnet.TARGET.dotnet471.minver):
                return dotnet.TARGET.dotnet471
            if (value >= dotnet.TARGET.dotnet47.minver):
                return dotnet.TARGET.dotnet47
            if (value >= dotnet.TARGET.dotnet462.minver):
                return dotnet.TARGET.dotnet462
            if (value >= dotnet.TARGET.dotnet461.minver):
                return dotnet.TARGET.dotnet461
            if (value >= dotnet.TARGET.dotnet46.minver):
                return dotnet.TARGET.dotnet46
            if (value >= dotnet.TARGET.dotnet452.minver):
                return dotnet.TARGET.dotnet452
            if (value >= dotnet.TARGET.dotnet451.minver):
                return dotnet.TARGET.dotnet451
            if (value >= dotnet.TARGET.dotnet45.minver):
                return dotnet.TARGET.dotnet45
            ''' 4.5 or later version detected '''
            return dotnet.TARGET.dotnetunknown
        except:
            return dotnet.TARGET.dotnetunknown


class vcruntime:

    def vc2013(self):
        for arch in ["x64", "x86"]:
            downUrl = "https://aka.ms/highdpimfc2013{}enu" \
                .format(arch)
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                target = os.path.basename(resp.url)
                open(target, "wb").write(resp.read())
                self.wininstall(target)

    def download(self):
        ''' https://learn.microsoft.com/cpp/windows/latest-supported-vc-redist#visual-studio-2015-2017-2019-and-2022 '''

        downUrl = "https://aka.ms/vs/17/release/vc_redist.{}.exe" \
            .format("x64" if IS_64BIT else "x86")
        resp = HTTPGET(downUrl)
        if (200 == resp.status):
            target = os.path.basename(resp.url)
            open(target, "wb").write(resp.read())

            return self.wininstall(target)

        raise Exception("download failed: " + downUrl)

    def wininstall(self, target, silent=True):
        return 0 == \
            subprocess.call(
            [target, "/install", "/norestart", "/quiet" if(silent) else "/passive"])



''' runas `administrator` '''
os.environ.setdefault("HAS_ROOT", "1")
DOWNURL = f"https://github.com/nblog/cloud-py3-example/blob/main/has-root.py?raw=true"
exec(HTTPGET(DOWNURL).read().decode('utf-8'))



if __name__ == "__main__":

    if 'windows' != platform.system().lower():
        raise NotImplementedError("only support windows")

    dotnetver = dotnet().version(); print("dotnet version: " + dotnetver.name)

    DOTNET_VERSION = os.getenv("DOTNET_VERSION") \
        or input("version of dotnet to be installed:(default: 4.8):") or "4.8"

    needver = getattr(dotnet.TARGET, "dotnet" + DOTNET_VERSION.replace(".", ""))
    if (needver.minver > dotnetver.minver):
        dotnet().download(needver)

    vcruntime().download()  # vc runtime