#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, re, platform, urllib.request, subprocess


HTTPGET = urllib.request.urlopen


class frida_gadget:

    RELEASES_URL = "https://github.com/frida/frida/releases"

    class TARGET:
        system = dict({
            "darwin": "macos",
        }).get(platform.system().lower(), platform.system().lower())

    def latest(self):
        resp = HTTPGET( "/".join([self.RELEASES_URL, "latest"]) )
        tagVer = str(resp.url).split("tag/")[-1]
        return tagVer

    def assets(self, tagVer, system=TARGET):
        resp = HTTPGET( "/".join([self.RELEASES_URL, "expanded_assets", tagVer]) )
        assets = re.findall(">(frida-gadget-.*?)<", resp.read().decode())
        return [asset for asset in assets if system.system in asset]

    def download(self, tagVer="latest"):
        if tagVer == "latest": tagVer = self.latest()

        for target in self.assets(tagVer):
            downUrl = "/".join([self.RELEASES_URL, "download", tagVer, target])
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                self.extract(resp.read(), target)

        return True
        raise Exception("download failed: " + downUrl)

    def extract(self, data, target, target_dir=''):
        import lzma
        target = os.path.join(target_dir, os.path.splitext(target)[0])
        open(target, "wb").write(lzma.decompress(data))
        return os.path.join(os.getcwd(), target)

class frida_server:

    RELEASES_URL = "https://github.com/frida/frida/releases"

    class TARGET:
        B64 = bool(sys.maxsize > 2**32)

        arch = "x86_64" if B64 else "x86"

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
                if system.system in asset and system.arch in asset]

    def download(self, tagVer="latest"):
        if tagVer == "latest": tagVer = self.latest()
        target = self.assets(tagVer)[0]
        downUrl = "/".join([self.RELEASES_URL, "download", tagVer, target])
        resp = HTTPGET(downUrl)
        if (200 == resp.status):
            return self.extract(resp.read(), target)

        raise Exception("download failed: " + downUrl)

    def extract(self, data, target, target_dir=''):
        import lzma
        target = os.path.join(target_dir, os.path.splitext(target)[0])
        open(target, "wb").write(lzma.decompress(data))
        return os.path.join(os.getcwd(), target)

    def run(self, argv=[], binpath=''):
        self.app = subprocess.Popen([binpath]+argv)



if __name__ == "__main__":

    FRIDA_VERSION = os.environ.get("FRIDA_VERSION", "latest")

    ''' default listen: all ipv4 (0.0.0.0:27042)  all ipv6 (::) '''
    FRIDA_SERVER_PORT = os.environ.get("FRIDA_SERVER_PORT", "27042")

    cmd = ["--listen", ':'.join(["0.0.0.0", FRIDA_SERVER_PORT])]

    if ("FRIDA_SERVER_TOKEN" in os.environ):
        cmd += ["--token", os.environ["FRIDA_SERVER_TOKEN"]]

    app = frida_server(); app.run(cmd, app.download(FRIDA_VERSION))

    ''' reserved for frpc '''
    os.environ["FRPC_LOCAL_PORT"] = FRIDA_SERVER_PORT