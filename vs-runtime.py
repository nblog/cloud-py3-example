#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, re, platform, urllib.request, subprocess


HTTPGET = urllib.request.urlopen


B64 = bool(sys.maxsize > 2**32)


class dotnet:

    class TARGET:
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

        dotnetver = dotnet481


    def download(self, dotnetver=TARGET.dotnet481):
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

    def win7sp1(self):
        ''' https://learn.microsoft.com/archive/blogs/vsnetsetup/a-certificate-chain-could-not-be-built-to-a-trusted-root-authority-2 '''
        ''' reboot / KB2813430: https://download.microsoft.com/download/F/D/B/FDB0E76D-2C15-45D1-A49B-BFB405008569/Windows6.1-KB2813430-x64.msu '''

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
                return dotnet.TARGET.dotnet481.name
            if (value >= dotnet.TARGET.dotnet48.minver):
                return dotnet.TARGET.dotnet48.name
            if (value >= dotnet.TARGET.dotnet472.minver):
                return dotnet.TARGET.dotnet472.name
            if (value >= dotnet.TARGET.dotnet471.minver):
                return dotnet.TARGET.dotnet471.name
            if (value >= dotnet.TARGET.dotnet47.minver):
                return dotnet.TARGET.dotnet47.name
            if (value >= dotnet.TARGET.dotnet462.minver):
                return dotnet.TARGET.dotnet462.name
            if (value >= dotnet.TARGET.dotnet461.minver):
                return dotnet.TARGET.dotnet461.name
            if (value >= dotnet.TARGET.dotnet46.minver):
                return dotnet.TARGET.dotnet46.name
            if (value >= dotnet.TARGET.dotnet452.minver):
                return dotnet.TARGET.dotnet452.name
            if (value >= dotnet.TARGET.dotnet451.minver):
                return dotnet.TARGET.dotnet451.name
            if (value >= dotnet.TARGET.dotnet45.minver):
                return dotnet.TARGET.dotnet45.name
            return "unknown"
        except:
            return "unavailable"


class vcruntime:

    def download(self):
        ''' https://learn.microsoft.com/cpp/windows/latest-supported-vc-redist#visual-studio-2015-2017-2019-and-2022 '''

        downUrl = "https://aka.ms/vs/17/release/vc_redist.{}.exe" \
            .format("x64" if(B64) else "x86")
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


if __name__ == "__main__":

    if 'windows' != platform.system().lower():
        raise NotImplementedError("only support windows")

    print("dotnet version: " + dotnet().version())

    DOTNET_VERSION = os.environ.get("DOTNET_VERSION") \
        or input("version of dotnet to be installed:(default: 4.8):") or "4.8"

    dotnet().download( \
        getattr(dotnet.TARGET, "dotnet" + DOTNET_VERSION.replace(".", "")))

    vcruntime().download()