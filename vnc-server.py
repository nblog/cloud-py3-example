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

    def wininstall(self):
        raise NotImplementedError("not implemented yet")


class realvnc:

    class vncver:
        vnc6 = "6.11.0"

    TARGET = dict({
        "windows": "VNC-Server-{vncver}-Windows-msi.zip",
        "linux": "VNC-Server-{vncver}-Linux-x64.deb",
        "darwin": "VNC-Server-{vncver}-MacOSX-universal.pkg",
        "raspberrypi": "VNC-Server-{vncver}-ARM64.deb",
    })[platform.system().lower()]

    def download(self, tagVer=vncver.vnc6):
        downUrl = "https://downloads.realvnc.com/download/file/vnc.files/" + \
            self.TARGET.format(vncver=tagVer)
        resp = HTTPGET(downUrl)
        if (200 == resp.status):
            if "windows" == platform.system().lower():
                return self.wininstall(resp.read(), os.path.basename(downUrl))
            elif "linux" == platform.system().lower():
                return self.linuxinstall(resp.read(), os.path.basename(downUrl))
            else:
                raise NotImplementedError("not implemented yet")

        raise Exception("download failed: " + downUrl)

    def wininstall(self, data=b'', target='', silent=True):
        import io, sys, zipfile; zipfile.ZipFile(io.BytesIO(data)).extractall()
        b64 = bool(sys.maxsize > 2**32)
        msi = list(filter(lambda x: x.endswith( \
            "64bit.msi" if (b64) else "32bit.msi"), os.listdir()))[0]
        subprocess.check_call(
            ["msiexec", "/i", msi, "/quiet" if silent else "/passive"])

        target = os.path.join(
            os.environ["ProgramFiles" + ("" if (b64) else "(x86)")],
            "RealVNC", "VNC Server")

        ''' register '''
        if ("realvnc_token" in os.environ):
            subprocess.call([
                os.path.join(target, "vnclicense"), 
                "-add", os.environ["realvnc_token"].strip('\"')], cwd=target)

        return target

    def linuxinstall(self, data=b'', target='', silent=True):
        open(target, "wb").write(data)
        subprocess.check_call(["dpkg", "-i", target])

        raise NotImplementedError("not implemented yet") 


if __name__ == "__main__":

    realvnc().download()