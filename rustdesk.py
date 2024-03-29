#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, re, platform, urllib.request, subprocess


HTTPGET = urllib.request.urlopen


B64 = bool(sys.maxsize > 2**32)


class rustdesk:

    RELEASES_URL = "https://github.com/rustdesk/rustdesk/releases"

    class TARGET:
        arch = dict({
            "x86": "x32", "x86_64": "x64",
            "i386": "x32", "amd64": "x64",
        }).get(platform.machine().lower(), platform.machine().lower())

        system = platform.system().lower()


    def latest(self):
        resp = HTTPGET( "/".join([self.RELEASES_URL, "latest"]) )
        tagVer = str(resp.url).split("tag/")[-1]
        return tagVer

    def assets(self, tagVer):
        resp = HTTPGET( "/".join([self.RELEASES_URL, "expanded_assets", tagVer]) )
        assets = re.findall(">(rustdesk-.*?)<", resp.read().decode())
        return assets

    def download(self, tagVer="latest"):
        raise NotImplementedError

    def winrun(self, argv=[], binpath="."):
        self.app = subprocess.Popen([binpath]+argv)



if __name__ == "__main__":

    # ''' default configuration '''
    # from configparser import ConfigParser
    # cfg = ConfigParser()
    # cfg["options"] = {}
    # cfg["options"]["stop-service"] = repr("Y")
    # cfg["options"]["direct-server"] = repr("Y")

    # if ("rustdesk_direct_port" in os.environ):
    #     cfg["options"]["direct-access-port"] = repr(os.environ["rustdesk_direct_port"])

    # cfgdir = os.path.join(os.environ["APPDATA"], "RustDesk", "config")
    # os.makedirs(cfgdir, exist_ok=True)
    # cfg.write(open(os.path.join(cfgdir, "RustDesk2.toml"), "w"))


    app = rustdesk(); app.winrun([], app.download()); app.app.wait()