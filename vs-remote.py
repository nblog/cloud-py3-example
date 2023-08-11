#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, re, platform, urllib.request, subprocess


HTTPGET = urllib.request.urlopen


B64 = bool(sys.maxsize > 2**32)


class vs_remote:
    '''
        https://learn.microsoft.com/visualstudio/debugger/remote-debugger-port-assignments
        2022: 4026 / 4027
        2019: 4024 / 4025
        2017: 4022 / 4023
        2015: 4020 / 4021
        2013: 4018 / 4019
        2012: 4016 / 4017
        2008/2010: 4015
    '''

    class TARGET:
        class enum_language:
            en_us, zh_cn, zh_tw = "enu", "chs", "cht"

        class enum_arch:
            ARM64, AMD64, I386 =  "arm64", "amd64", "x86"

        class enum_vsver:
            vs2017, vs2019, vs2022 = 15, 16, 17
            vs2012, vs2013, vs2015 = 11, 12, 14
            vs2008, vs2010 = 9, 10

        vsver = enum_vsver.vs2022
        arch = enum_arch.AMD64
        language = enum_language.en_us

    def vs2008(self):
        return "https://download.microsoft.com/download/9/8/2/98220c80-1633-4297-8b02-a8af777057b8/rdbgsetup_x64.exe"

    def vs2010(self):
        return "https://download.microsoft.com/download/E/E/1/EE10FC0E-8408-4C09-B9EB-4684160CFEE2/rdbgsetup_x64.exe"

    def vs2012(self):
        return "https://download.microsoft.com/download/4/1/5/41524F91-4CEE-416B-BB70-305756373937/VSU4/rtools_setup_x64.exe"

    def vs2013(self):
        return "https://download.microsoft.com/download/6/F/8/6F8AEDBF-E027-492A-9009-DB38788BBA02/rtools_setup_x64.exe"

    def vs2015(self):
        return "https://download.microsoft.com/download/E/7/A/E7AEA696-A4EB-48DD-BA4A-9BE41A402400/rtools_setup_x64.exe"

    def download(self, vsVer: int):
        vs_remote.TARGET.vsver = vsVer

        downUrl = f"https://aka.ms/vs/{vs_remote.TARGET.vsver}/release/" \
            f"RemoteTools.{vs_remote.TARGET.arch}ret.{vs_remote.TARGET.language}.exe"

        if (vsVer == vs_remote.TARGET.enum_vsver.vs2008):
            downUrl = self.vs2008()
        if (vsVer == vs_remote.TARGET.enum_vsver.vs2010):
            downUrl = self.vs2010()
        if (vsVer == vs_remote.TARGET.enum_vsver.vs2012):
            downUrl = self.vs2012()
        if (vsVer == vs_remote.TARGET.enum_vsver.vs2013):
            downUrl = self.vs2013()
        if (vsVer == vs_remote.TARGET.enum_vsver.vs2015):
            downUrl = self.vs2015()

        resp = HTTPGET(downUrl)
        if (200 == resp.status):
            target = os.path.basename(resp.url)
            open(target, "wb").write(resp.read())

            return self.wininstall(target)

        raise Exception("download failed: " + downUrl)

    def wininstall(self, target, silent=False):
        subprocess.check_call(
            [target, "/install", "/norestart", "/quiet" if silent else "/passive"])
        return os.path.join(
                os.environ["ProgramFiles"], 
                f"Microsoft Visual Studio {vs_remote.TARGET.vsver}.0", 
                "Common7", "IDE", "Remote Debugger",
                # https://docs.python.org/3/library/platform.html?highlight=is_64bits#platform.architecture
                "x64" if (B64) else "x86")

    def winrun(self, argv=[], target_dir='.'):
        app = os.path.join(target_dir, "msvsmon.exe")
        self.app = subprocess.Popen([app]+argv, cwd=target_dir)



if __name__ == "__main__":

    if 'windows' != platform.system().lower():
        raise NotImplementedError("only support windows")

    cmd = ["/installed"] + [
        "/noauth", "/anyuser", "/nosecuritywarn",
        "/nofirewallwarn"
    ]

    cmd += ["/timeout", str(3 * 86400)]
    # cmd += ["/timeout", input("maximum idle time, seconds(default:3 hours):") or str(3 * 3600)]

    # ''' default port is different '''
    # if ("vsremote_port" in os.environ):
    #     cmd += ["/port", os.environ["vsremote_port"]]

    app = vs_remote(); vsver = \
        getattr(vs_remote.TARGET.enum_vsver, input("vs version(default:vs2022):") or "vs2022")
    app.winrun(cmd, app.download(vsver)); app.app.wait()