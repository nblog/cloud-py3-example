#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, platform, urllib.request, subprocess
import sys, locale


HTTPGET = urllib.request.urlopen


class vs_remote:

    class enum_language:
        en_us, zh_cn, zh_tw = "enu", "chs", "cht"

    class enum_arch:
        ARM64, AMD64, I386 =  "arm64", "amd64", "x86"

    class enum_vsver:
        vs2017, vs2019, vs2022 = 15, 16, 17

    DEFAULT_ARCH = dict({
        "x86_64": enum_arch.AMD64,
        "i386": enum_arch.I386,
    }).get(platform.machine().lower(), platform.machine().lower())

    DEFAULT_LANGUAGE = getattr(enum_language, locale.getdefaultlocale()[0].lower(), "enu")

    TARGET = \
        "https://aka.ms/vs/{vsver}/release/RemoteTools.{arch}ret.{language}.exe"

    def download(self, vsVer=enum_vsver.vs2022):
        downUrl = self.TARGET.format(
            vsver=vsVer, arch=self.DEFAULT_ARCH, language=self.DEFAULT_LANGUAGE)
        resp = HTTPGET(downUrl)
        if (200 == resp.status):
            remotedbgDir = os.path.join(
                os.environ["ProgramFiles"], 
                f"Microsoft Visual Studio {vsVer}.0", 
                "Common7", "IDE", "Remote Debugger",
                # https://docs.python.org/3/library/platform.html?highlight=is_64bits#platform.architecture
                "x64" if (bool(sys.maxsize > 2**32)) else "x86")
            self.install(resp.read()); return remotedbgDir

        raise Exception("download failed: " + downUrl)

    def install(self, data, silent=True):
        open("remotetools.exe", "wb").write(data)
        subprocess.check_call(
            ["remotetools.exe"] + ["/install", "/norestart", "/quiet" if silent else "/passive"])

    def winrun(self, argv=[], pathdir="."):
        app = "\"" + os.path.join(pathdir, "msvsmon.exe") + "\""
        self.app = subprocess.Popen(' '.join([app] + argv))



if __name__ == "__main__":

    cmd = ["/installed"] + [
        "/timeout", os.environ.get("vsremote_timeout", str(3 * 86400)),
        "/port", os.environ.get("vsremote_port", "4026"),
        "/noauth", "/anyuser", "/nosecuritywarn"
    ]

    app = vs_remote(); vsver = int(os.environ.get("vsremote_version", "17"))
    app.winrun(cmd, app.download(vsver)); app.app.wait()