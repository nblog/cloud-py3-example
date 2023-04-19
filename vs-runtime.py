#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, re, platform, urllib.request, subprocess


HTTPGET = urllib.request.urlopen


B64 = bool(sys.maxsize > 2**32)


class dotnet:

    class TARGET:
        class enum_dotnetver:
            dotnet45 = "45"
            dotnet451 = "451"
            dotnet452 = "452"
            dotnet46 = "46"
            dotnet461 = "461"
            dotnet462 = "462"
            dotnet47 = "47"
            dotnet471 = "471"
            dotnet472 = "472"
            dotnet48 = "48"
            dotnet481 = "481"
        dotnetver = enum_dotnetver.dotnet481


    def download(self, dotnetver=TARGET.enum_dotnetver.dotnet48):
        ''' https://dotnet.microsoft.com/download/dotnet-framework '''
        dotnet.TARGET.dotnetver = dotnetver

        downUrl = f"https://dotnet.microsoft.com/download/dotnet-framework/thank-you/net{dotnet.TARGET.dotnetver}-offline-installer"
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
            [target] + ["/q", "/norestart"] if(silent) else ["/passive", "/promptrestart"])

    def version(self):
        ''' https://learn.microsoft.com/dotnet/framework/migration-guide/how-to-determine-which-versions-are-installed#minimum-version '''
        import winreg
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\NET Framework Setup\NDP\v4\Full")
            value = winreg.QueryValueEx(key, "Release")[0]
            if (value >= 528040):
                return dotnet.TARGET.enum_dotnetver.dotnet48
            elif (value >= 461808):
                return dotnet.TARGET.enum_dotnetver.dotnet472
            elif (value >= 461308):
                return dotnet.TARGET.enum_dotnetver.dotnet471
            elif (value >= 460798):
                return dotnet.TARGET.enum_dotnetver.dotnet47
            elif (value >= 394802):
                return dotnet.TARGET.enum_dotnetver.dotnet462
            elif (value >= 394254):
                return dotnet.TARGET.enum_dotnetver.dotnet461
            elif (value >= 393295):
                return dotnet.TARGET.enum_dotnetver.dotnet46
            elif (value >= 379893):
                return dotnet.TARGET.enum_dotnetver.dotnet452
            elif (value >= 378675):
                return dotnet.TARGET.enum_dotnetver.dotnet451
            elif (value >= 378389):
                return dotnet.TARGET.enum_dotnetver.dotnet45
            else:
                return "not supported"
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

    if "windows" != platform.system().lower():
        raise Exception("only support windows")

    print("dotnet version: " + ("net"+dotnet().version()))

    vcruntime().download(), dotnet().download()