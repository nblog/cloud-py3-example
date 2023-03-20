#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, platform, urllib.request, subprocess


HTTPGET = urllib.request.urlopen


import sys, re
B64 = bool(sys.maxsize > 2**32)


class tightvnc:

    TARGET = \
        "https://www.tightvnc.com/download/{tagVer}/tightvnc-{tagVer}-gpl-setup-" + \
        "64bit.msi" if (B64) else "32bit.msi"

    def latest(self):
        resp = HTTPGET("https://www.tightvnc.com/download.php")
        tagVer = re.findall(r"tightvnc-(\d+\.\d+\.\d+)-gpl-setup", resp.read().decode())[0]
        return tagVer

    def download(self, tagVer="latest"):
        if tagVer == "latest": tagVer = self.latest()
        downUrl = self.TARGET.format(tagVer=tagVer)
        resp = HTTPGET(downUrl)
        if (200 == resp.status):
            return self.wininstall(resp.read(), os.path.basename(downUrl))

        raise Exception("download failed: " + downUrl)

    def wininstall(self, data=b'', target=''):
        ''' https://www.tightvnc.com/docs.php '''
        open(target, "wb").write(data)

        ''' default password '''
        if (not "tightvnc_passwd" in os.environ):
            os.environ.setdefault("tightvnc_passwd", "123456")

        ''' "SET_RFBPORT=1", "VALUE_OF_RFBPORT=5900" '''
        subprocess.check_call(
            ["msiexec", "/i", target, "/quiet", "/norestart"] + \
            ["SET_USEVNCAUTHENTICATION=1", "VALUE_OF_USEVNCAUTHENTICATION=1",
            "SET_PASSWORD=1", "VALUE_OF_PASSWORD=" + os.environ["tightvnc_passwd"]])

        target = os.path.join(
            os.environ["ProgramFiles" + ("" if (B64) else "(x86)")],
            "TightVNC")

        return target



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
        msi = list(filter(lambda x: x.endswith( \
            "64bit.msi" if (B64) else "32bit.msi"), os.listdir()))[0]
        subprocess.check_call(
            ["msiexec", "/i", msi, "/quiet" if silent else "/passive", "/norestart"])

        target = os.path.join(
            os.environ["ProgramFiles" + ("" if (B64) else "(x86)")],
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

    if "realvnc_token" in os.environ:
        realvnc().download()
    else:
        tightvnc().download()

