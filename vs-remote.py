#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, re, platform, urllib.request, subprocess


HTTPGET = urllib.request.urlopen


B64 = bool(sys.maxsize > 2**32)


class vs_remote:

    class TARGET:
        class enum_language:
            en_us, zh_cn, zh_tw = "enu", "chs", "cht"

        class enum_arch:
            ARM64, AMD64, I386 =  "arm64", "amd64", "x86"

        class enum_vsver:
            vs2017, vs2019, vs2022 = 15, 16, 17

        vsver = enum_vsver.vs2022
        arch = enum_arch.AMD64
        language = enum_language.en_us


    def download(self, vsVer=TARGET.enum_vsver.vs2022):
        vs_remote.TARGET.vsver = vsVer

        downUrl = f"https://aka.ms/vs/{vs_remote.TARGET.vsver}/release/" \
            f"RemoteTools.{vs_remote.TARGET.arch}ret.{vs_remote.TARGET.language}.exe"
        resp = HTTPGET(downUrl)
        if (200 == resp.status):
            return self.wininstall(resp.read())

        raise Exception("download failed: " + downUrl)

    def wininstall(self, data, silent=True):
        open("remotetools.exe", "wb").write(data)
        subprocess.check_call(
            ["remotetools.exe"] + ["/install", "/norestart", "/quiet" if silent else "/passive"])
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

    if "windows" != platform.system().lower():
        raise Exception("only support windows")

    cmd = ["/installed"] + [
        "/timeout", os.environ.get("vsremote_timeout", str(3 * 86400)),
        "/noauth", "/anyuser", "/nosecuritywarn",
        "/nofirewallwarn"
    ]

    ''' default port is different '''
    if ("vsremote_port" in os.environ):
        cmd += ["/port", os.environ["vsremote_port"]]

    app = vs_remote(); vsver = int(os.environ.get("vsremote_version", "17"))
    app.winrun(cmd, app.download(vsver)); app.app.wait()