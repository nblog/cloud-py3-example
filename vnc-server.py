#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, re, platform, urllib.request, subprocess


HTTPGET = urllib.request.urlopen


B64 = bool(sys.maxsize > 2**32)


class tightvnc:

    def latest(self):
        resp = HTTPGET("https://www.tightvnc.com/download.php")
        tagVer = re.findall(r"tightvnc-(\d+\.\d+\.\d+)-gpl-setup", resp.read().decode())[0]
        return tagVer

    def download(self, tagVer="latest"):
        if tagVer == "latest": tagVer = self.latest()
        downUrl = f"https://www.tightvnc.com/download/{tagVer}/tightvnc-{tagVer}-gpl-setup-" + \
        "64bit.msi" if (B64) else "32bit.msi"
        resp = HTTPGET(downUrl)
        if (200 == resp.status):
            target = os.path.basename(resp.url)
            open(target, "wb").write(resp.read())

            return self.wininstall(target)

        raise Exception("download failed: " + downUrl)

    def wininstall(self, target):
        ''' https://www.tightvnc.com/docs.php '''

        ''' default password: 123456 '''
        INSTALLCFG = [
            "SET_USEVNCAUTHENTICATION=1", "VALUE_OF_USEVNCAUTHENTICATION=1",
            "SET_PASSWORD=1", "VALUE_OF_PASSWORD=" + os.environ.get("tightvnc_passwd", "123456"),
            # "SET_RFBPORT=1", "VALUE_OF_RFBPORT=5900",
        ]
        subprocess.check_call(["msiexec", "/i", target, "/quiet", "/norestart"] + INSTALLCFG)

        return os.path.join(os.environ["ProgramFiles"], "TightVNC")



if __name__ == "__main__":

    tightvnc().download()
