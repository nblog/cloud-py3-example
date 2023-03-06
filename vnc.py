#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, platform, urllib.request, subprocess


HTTPGET = urllib.request.urlopen


class ultravnc:
    '''  '''

    TARGET = "https://uvnc.com/component/jdownloads/send/0-/436-ultravnc-1-4-06-bin-zip.html"

    def download(self, tagVer="1.4.0.6"):
        downUrl = self.TARGET.format(vncver=tagVer)
        resp = HTTPGET(downUrl)
        if (200 == resp.status):
            return self.wininstall(resp.read())

        raise Exception("download failed: " + downUrl)

    def wininstall(self, data, silent=True):
        raise NotImplementedError("Not implemented yet")


class realvnc:

    class enum_platform:
        win, macos, linux, raspberrypi = \
            "Windows-msi.zip", "MacOSX-universal.pkg", \
            "Linux-x64.deb", "ARM64.deb"

    class vncver:
        vnc6 = "6.11.0"

    TARGET = \
        "https://downloads.realvnc.com/download/file/vnc.files/VNC-Server-{vncver}-{platform}"

    def download(self, tagVer=enum_platform.win):
        downUrl = self.TARGET.format(vncver=self.vncver.vnc6, platform=tagVer)
        resp = HTTPGET(downUrl)
        if (200 == resp.status):
            return self.wininstall(resp.read())

        raise Exception("download failed: " + downUrl)

    def wininstall(self, data, silent=True):
        import io, sys, zipfile; zipfile.ZipFile(io.BytesIO(data)).extractall()
        b64 = bool(sys.maxsize > 2**32)
        msi = list(filter(lambda x: x.endswith( \
            "64bit.msi" if (b64) else "32bit.msi"), os.listdir()))[0]
        subprocess.check_call(
            ["msiexec", "/i", msi, "/quiet" if silent else "/passive"])

        ''' register '''
        target = os.path.join(
            os.environ["ProgramFiles" + ("" if (b64) else "(x86)")],
            "RealVNC", "VNC Server")
        subprocess.check_call(
            [os.path.join(target, "vnclicense"), "-add", os.environ["realvnc_key"]])
        return target



if __name__ == "__main__":

    app = realvnc().download()