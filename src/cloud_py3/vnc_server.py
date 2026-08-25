#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, io, sys, re, platform, subprocess

from cloud_py3._common import (
    EXTRACT, IS_64BIT, HTTPGET, download2
)

'''
https://github.com/ultravnc/UltraVNC
https://github.com/TurboVNC/turbovnc
'''


class tightvnc:
    ''' https://github.com/TigerVNC/tigervnc '''
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
            "SET_PASSWORD=1", "VALUE_OF_PASSWORD=" + os.getenv("TIGHTVNC_PASSWD", "123456"),
            # "SET_RFBPORT=1", "VALUE_OF_RFBPORT=os.getenv("VNC_SERVER_PORT", "5900")",
        ]
        subprocess.check_call(["msiexec", "/i", target, "/quiet", "/norestart"] + INSTALLCFG)


class realvnc:

    class vncver:
        vnc6 = "6.11.0"

    TARGET = dict({
        # http://web.archive.org/web/20251201110915/https://downloads.realvnc.com/download/file/viewer.files/VNC-Viewer-7.15.1-Windows-msi.zip
        # http://web.archive.org/web/20230329142406/https://downloads.realvnc.com/download/file/vnc.files/VNC-Server-6.11.0-Windows-msi.zip
        "windows": "VNC-Server-{vncver}-Windows-msi.zip",
        "linux": "VNC-Server-{vncver}-Linux-x64.deb",
        "darwin": "VNC-Server-{vncver}-MacOSX-universal.pkg",
        "raspberrypi": "VNC-Server-{vncver}-ARM64.deb",
    })[platform.system().lower()]

    def download(self, tagVer=vncver.vnc6):
        if "windows" == platform.system().lower():
            downUrl = "https://github.com/GTHF/trash_package/raw/refs/heads/main/" + \
                self.TARGET.format(vncver=tagVer)
            ARCH = "64bit" if (IS_64BIT) else "32bit"
            EXTRACT.zip(download2(downUrl), target_dir='.')
            target = f"VNC-Server-{tagVer}-Windows-en-{ARCH}.msi"

            return self.wininstall(target)
        elif "linux" == platform.system().lower():
            raise NotImplementedError("not implemented yet")
        else:
            raise NotImplementedError("not implemented yet")

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


def main():
    ''' to execute, runas `administrator` '''
    from cloud_py3.has_root import has_root, main as has_root_main
    os.environ.setdefault("HAS_ROOT", "1")
    has_root_main()

    realvnc().download()

    os.environ["EXEC_LOCAL_PORT"] = os.getenv("VNC_SERVER_PORT", "5900")


if __name__ == "__main__":
    main()
