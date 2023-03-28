#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, re, platform, urllib.request, subprocess


HTTPGET = urllib.request.urlopen


class frida_server:

    RELEASES_URL = os.environ.get("GHPROXY","") + \
        "https://github.com/frida/frida/releases"

    class TARGET:
        arch = dict({
            "i386": "x86", "i686": "x86",
            "amd64": "x86_64",
        }).get(platform.machine().lower(), platform.machine().lower())

        system = dict({
            "darwin": "macos",
        }).get(platform.system().lower(), platform.system().lower())


    def latest(self):
        resp = HTTPGET( "/".join([self.RELEASES_URL, "latest"]) )
        tagVer = str(resp.url).split("tag/")[-1]
        return tagVer

    def assets(self, tagVer, system=TARGET):
        resp = HTTPGET( "/".join([self.RELEASES_URL, "expanded_assets", tagVer]) )
        assets = re.findall(">(frida-server-.*?)<", resp.read().decode())
        return [asset for asset in assets \
                if system.arch in asset and system.system in asset]

    def download(self, tagVer="latest"):
        if tagVer == "latest": tagVer = self.latest()
        target = self.assets(tagVer)[0]
        downUrl = "/".join([self.RELEASES_URL, "download", tagVer, target])
        resp = HTTPGET(downUrl)
        if (200 == resp.status):
            return self.extract(resp.read(), target)

        raise Exception("download failed: " + downUrl)

    def extract(self, data, target=''):
        import lzma; name = os.path.splitext(target)[0]
        open(name, "wb").write(lzma.decompress(data))
        return os.path.join(os.getcwd(), name)

    def run(self, argv=[], binpath=''):
        self.app = subprocess.Popen([binpath]+argv)



if __name__ == "__main__":

    cmd = []
    if ("frida_server_listen" in os.environ):
        ''' default: 0.0.0.0:27042 '''
        cmd += ["--listen", os.environ["frida_server_listen"]]
    if ("frida_server_token" in os.environ):
        cmd += ["--token", os.environ["frida_server_token"].strip('\"')]

    app = frida_server()
    app.run(cmd, app.download()); app.app.wait()