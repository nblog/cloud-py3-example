#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, io, sys, re, types, platform, subprocess, urllib.request

HTTPGET = urllib.request.urlopen

if not bool(os.environ.get("DEBUGPY_RUNNING")):
    target = "utils/common"
    RAW_CODE = HTTPGET(f"https://github.com/nblog/cloud-py3-example/blob/main/{target}.py?raw=true").read().decode('utf-8')

    raw_module = types.ModuleType('common')
    sys.modules['utils.common'] = raw_module
    exec(RAW_CODE, raw_module.__dict__)

from utils.common import (
    EXTRACT,
    IS_64BIT,
)


class tightvnc:

    def latest(self):
        resp = HTTPGET("https://www.tightvnc.com/download.php")
        tagVer = re.findall(r"tightvnc-(\d+\.\d+\.\d+)-gpl-setup", resp.read().decode())[0]
        return tagVer

    def has_installed(self):
        INSTALL_DIR = os.path.join(
                os.environ["ProgramFiles"], 
                "TightVNC")
        return (os.path.exists(INSTALL_DIR), INSTALL_DIR)

    def download(self, tagVer="latest"):
        installed = self.has_installed()
        if (installed[0]): return installed[1]

        if tagVer == "latest": tagVer = self.latest()
        downUrl = f"https://www.tightvnc.com/download/{tagVer}/tightvnc-{tagVer}-gpl-setup-" + \
        "64bit.msi" if (IS_64BIT) else "32bit.msi"
        resp = HTTPGET(downUrl)
        if (200 == resp.status):
            target = os.path.basename(resp.url)
            open(target, "wb").write(resp.read())

            self.wininstall(target); return installed[1]

        raise Exception("download failed: " + downUrl)

    def wininstall(self, target):
        ''' https://www.tightvnc.com/docs.php '''

        ''' default password: 123456 '''
        INSTALLCFG = [
            "SET_USEVNCAUTHENTICATION=1", "VALUE_OF_USEVNCAUTHENTICATION=1",
            "SET_PASSWORD=1", "VALUE_OF_PASSWORD=" + os.environ.get("TIGHTVNC_PASSWD", "123456"),
            # "SET_RFBPORT=1", "VALUE_OF_RFBPORT=os.environ.get("VNC_SERVER_PORT", "5900")",
        ]
        subprocess.check_call(["msiexec", "/i", target, "/quiet", "/norestart"] + INSTALLCFG)


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
                import io, zipfile
                ARCH = "64bit" if (IS_64BIT) else "32bit"
                target = zipfile.ZipFile(io.BytesIO(resp.read())).extract(
                    f"VNC-Server-{tagVer}-Windows-en-{ARCH}.msi")

                return self.wininstall(target)
            elif "linux" == platform.system().lower():
                raise NotImplementedError("not implemented yet")
            else:
                raise NotImplementedError("not implemented yet")

        raise Exception("download failed: " + downUrl)

    def wininstall(self, target, silent=True):
        subprocess.check_call(
            ["msiexec", "/i", target, "/quiet" if silent else "/passive", "/norestart"])

        target = os.path.join(
            os.environ["ProgramFiles" if (IS_64BIT) else "ProgramFiles(x86)"],
            "RealVNC", "VNC Server")

        ''' register '''
        subprocess.call([
            os.path.join(target, "vnclicense"), 
            "-add", "VKUPN-MTHHC-UDHGS-UWD76-6N36A"], cwd=target)

        return target



if __name__ == "__main__":

    tightvnc().download()

    os.environ["EXEC_LOCAL_PORT"] = os.environ.get("VNC_SERVER_PORT", "5900")