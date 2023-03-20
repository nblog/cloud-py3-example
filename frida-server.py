#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, platform, urllib.request, subprocess


HTTPGET = urllib.request.urlopen


class frida_server:

    RELEASES_URL = os.environ.get("GHPROXY","") + \
        "https://github.com/frida/frida/releases"

    DEFAULT_ARCH = dict({
        "i386": "x86",
        "amd64": "x86_64",
    }).get(platform.machine().lower(), platform.machine().lower())

    TARGET = dict({
        "windows": "frida-server-{tagVer}-windows-{arch}.exe.xz",
        "linux": "frida-server-{tagVer}-linux-{arch}.xz",
        "darwin": "frida-server-{tagVer}-macos-{arch}.xz",
    })[platform.system().lower()]

    def latest(self):
        resp = HTTPGET( "/".join([self.RELEASES_URL, "latest"]) )
        tagVer = str(resp.url).split("tag/")[-1]
        return tagVer

    def download(self, tagVer="latest"):
        if tagVer == "latest": tagVer = self.latest()
        downUrl = "/".join([
            self.RELEASES_URL, "download", tagVer, \
            self.TARGET.format(tagVer=tagVer, arch=self.DEFAULT_ARCH)])
        resp = HTTPGET(downUrl)
        if (200 == resp.status):
            return self.extract(resp.read(), os.path.basename(downUrl))

        raise Exception("download failed: " + downUrl)

    def extract(self, data=b'', target=''):
        import lzma; name = os.path.splitext(target)[0]
        open(name, "wb").write(lzma.decompress(data))
        return name

    def run(self, argv=[], binpath="."):
        app = os.path.join(".", binpath)
        self.app = subprocess.Popen([app]+argv)



if __name__ == "__main__":

    cmd = []
    if ("frida_server_listen" in os.environ):
        ''' default: 0.0.0.0:27042 '''
        cmd += ["--listen", os.environ["frida_server_listen"]]
    if ("frida_server_token" in os.environ):
        cmd += ["--token", os.environ["frida_server_token"].strip('\"')]

    app = frida_server()
    app.run(cmd, app.download()); app.app.wait()