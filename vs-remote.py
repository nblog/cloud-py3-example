#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, re, platform, urllib.request, subprocess


HTTPGET = urllib.request.urlopen

# https://docs.python.org/3/library/platform.html?highlight=is_64bits#platform.architecture
B64 = bool(sys.maxsize > 2**32)


class vs_remote:

    class TARGET:
        class enum_language:
            en_us, zh_cn, zh_tw = "enu", "chs", "cht"

        class enum_arch:
            ARM64, AMD64, I386 =  "arm64", "amd64", "x86"

        class enum_vsver:
            vs2017, vs2019, vs2022 = 15, 16, 17
            vs2012, vs2013, vs2015 = 11, 12, 14
            ''' below is no longer supported '''
            vs2008, vs2010 = 9, 10

        language = enum_language.en_us
        arch = os.environ['PROCESSOR_ARCHITECTURE'].startswith('ARM') and enum_arch.ARM64 or \
            (B64 and enum_arch.AMD64 or enum_arch.I386)
        vsver = enum_vsver.vs2022

    def vs2012(self):
        return "https://download.microsoft.com/download/4/1/5/41524F91-4CEE-416B-BB70-305756373937/VSU4/rtools_setup_x64.exe"

    def vs2013(self):
        return "https://download.microsoft.com/download/6/F/8/6F8AEDBF-E027-492A-9009-DB38788BBA02/rtools_setup_x64.exe"

    def vs2015(self):
        return "https://download.microsoft.com/download/E/7/A/E7AEA696-A4EB-48DD-BA4A-9BE41A402400/rtools_setup_x64.exe"

    def has_installed(self):
        INSTALL_DIR = os.path.join(
            os.environ["ProgramFiles(x86)"],
            f"Microsoft Visual Studio {vs_remote.TARGET.vsver}.0",
            "Common7", "IDE", "Remote Debugger")
        if (not os.path.exists(INSTALL_DIR)):
            INSTALL_DIR = os.path.join(
                    os.environ["ProgramFiles"], 
                    f"Microsoft Visual Studio {vs_remote.TARGET.vsver}.0", 
                    "Common7", "IDE", "Remote Debugger")
        return (os.path.exists(INSTALL_DIR), INSTALL_DIR)

    def download(self, vsVer: int):
        vs_remote.TARGET.vsver = vsVer

        installed = self.has_installed()
        if (installed[0]): return installed[1]

        downUrl = f"https://aka.ms/vs/{vs_remote.TARGET.vsver}/release/" \
            f"RemoteTools.{vs_remote.TARGET.arch}ret.{vs_remote.TARGET.language}.exe"

        if (vsVer == vs_remote.TARGET.enum_vsver.vs2012):
            downUrl = self.vs2012()
        if (vsVer == vs_remote.TARGET.enum_vsver.vs2013):
            downUrl = self.vs2013()
        if (vsVer == vs_remote.TARGET.enum_vsver.vs2015):
            downUrl = self.vs2015()

        resp = HTTPGET(downUrl)
        if (200 == resp.status):
            target = os.path.basename(resp.url); \
                open(target, "wb").write(resp.read())

            self.wininstall(target); return installed[1]

        raise Exception("download failed: " + downUrl)

    def wininstall(self, target, silent=False):
        subprocess.check_call(
            [target, "/install", "/norestart", "/quiet" if silent else "/passive"])

    def winrun(self, argv=[], target_dir='.'):
        if (os.environ['PROCESSOR_ARCHITECTURE'].startswith('ARM')):
            arch = (B64 and 'arm64' or 'arm')
        else:
            arch = (B64 and 'x64' or 'x86')
        app = os.path.join(target_dir, arch, "msvsmon.exe")
        self.app = subprocess.Popen([app]+argv, cwd=target_dir)



if __name__ == "__main__":

    if 'windows' != platform.system().lower():
        raise NotImplementedError("only support windows")

    cmd = ["/installed"] + [
        "/noauth", "/anyuser", "/nosecuritywarn",
        "/nofirewallwarn"
    ]

    cmd += ["/timeout", str(3 * 86400)] # 3 days

    ''' https://learn.microsoft.com/visualstudio/debugger/remote-debugger-port-assignments '''
    VSREMOTE_VER, VSREMOTE_PORT = 'vs2022', '4026'

    if ("VSREMOTE_PORT" in os.environ):
        cmd += ["/port", os.environ["VSREMOTE_PORT"]]; \
            VSREMOTE_PORT = os.environ["VSREMOTE_PORT"]

    app = vs_remote(); vsver = \
        getattr(vs_remote.TARGET.enum_vsver, input(f"vs version(default:{VSREMOTE_VER}):") or VSREMOTE_VER)
    app.winrun(cmd, app.download(vsver))

    if(vsver == vs_remote.TARGET.enum_vsver.vs2012):
        VSREMOTE_PORT = '4016'
    elif(vsver == vs_remote.TARGET.enum_vsver.vs2013):
        VSREMOTE_PORT = '4018'
    elif(vsver == vs_remote.TARGET.enum_vsver.vs2015):
        VSREMOTE_PORT = '4020'
    elif(vsver == vs_remote.TARGET.enum_vsver.vs2017):
        VSREMOTE_PORT = '4022'
    elif(vsver == vs_remote.TARGET.enum_vsver.vs2019):
        VSREMOTE_PORT = '4024'
    elif(vsver == vs_remote.TARGET.enum_vsver.vs2022):
        VSREMOTE_PORT = '4026'

    ''' reserved for frpc '''
    os.environ["FRPC_LOCAL_PORT"] = VSREMOTE_PORT

    '''
    The Visual Studio Remote Debugger cannot debug .NET code. 
    The remote debugger requires .NET Framework version 4.6.2 or newer to be installed. 
    This does not affect debugging native applications.
    '''
    if (input("need dotnet debugging support (y/n):").lower().startswith("y")):
        os.environ.setdefault("DOTNET_VERSION", "4.8")
        DOWNURL = f"https://github.com/nblog/cloud-py3-example/blob/main/vs-runtime.py?raw=true"
        exec(HTTPGET(DOWNURL).read().decode('utf-8'))