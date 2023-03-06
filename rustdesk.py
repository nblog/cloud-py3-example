#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, platform, urllib.request, subprocess


HTTPGET = urllib.request.urlopen


class rustdesk:

    RELEASES_URL = os.environ.get("GHPROXY","") + \
        "https://github.com/rustdesk/rustdesk/releases"

    DEFAULT_ARCH = dict({
        "x86": "x32", "x86_64": "x64",
        "i386": "x32", "amd64": "x64",
    }).get(platform.machine().lower(), platform.machine().lower())

    TARGET = dict({
        "windows": "rustdesk-{tagVer}-{arch}.exe",
        "linux": "rustdesk-{tagVer}.deb",
        "darwin": "rustdesk-{tagVer}.dmg",
    })[platform.system().lower()]

    def latest(self):
        res = HTTPGET( "/".join([self.RELEASES_URL, "latest"]) )
        tagVer = str(res.url).split("tag/")[-1]
        return tagVer

    def download(self, tagVer="latest"):
        if tagVer == "latest": tagVer = self.latest()
        downUrl = "/".join([
            self.RELEASES_URL, "download", tagVer, \
            self.TARGET.format(tagVer=tagVer, arch=self.DEFAULT_ARCH)])
        resp = HTTPGET(downUrl)
        if (200 == resp.status):
            target = os.path.basename(downUrl)
            open(target, "wb").write(resp.read())
            return target

    def winrun(self, argv=[], binpath="."):
        self.app = subprocess.Popen(' '.join([binpath] + argv))



if __name__ == "__main__":

    ''' default configuration '''
    from configparser import ConfigParser
    cfg = ConfigParser()
    cfg["options"] = {}
    cfg["options"]["stop-service"] = repr("Y")
    cfg["options"]["direct-server"] = repr("Y")
    cfg["options"]["direct-access-port"] = repr("21118")

    cfgdir = os.path.join(os.environ["APPDATA"], "RustDesk", "config")
    os.makedirs(cfgdir, exist_ok=True)
    cfg.write(open(os.path.join(cfgdir, "RustDesk2.toml"), "w"))


    app = rustdesk()
    app.winrun([], app.download())
    app.app.wait()