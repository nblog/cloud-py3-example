#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, platform, urllib.request, subprocess


HTTPGET = urllib.request.urlopen


class x64dbg:

    RELEASES_URL = os.environ.get("GHPROXY","") + \
        "https://github.com/x64dbg/x64dbg/releases"


    def latest(self):
        import re
        resp = HTTPGET( "/".join([self.RELEASES_URL, "latest"]) )
        tagVer = re.findall(">(snapshot[0-9\x2d\x5f]+).zip</h1>", resp.read().decode())[0]
        return tagVer

    def download(self, tagVer="latest"):
        if tagVer == "latest": tagVer = self.latest()
        downUrl = "/".join([
            self.RELEASES_URL, "download", f"snapshot/{tagVer}.zip"])
        resp = HTTPGET(downUrl)
        if (200 == resp.status):
            return self.extract(resp.read(), os.path.basename(downUrl))

        raise Exception("download failed: " + downUrl)

    def extract(self, data=b'', target=''):
        import io, zipfile
        zipfile.ZipFile(io.BytesIO(data)).extractall()
        return os.getcwd()


class die_engine:

    RELEASES_URL = os.environ.get("GHPROXY","") + \
        "https://github.com/horsicq/DIE-engine/releases"


    def latest(self):
        import re
        resp = HTTPGET( "/".join([self.RELEASES_URL, "latest"]) )
        tagVer = str(resp.url).split("tag/")[-1]
        return tagVer

    def download(self, tagVer="latest"):
        if tagVer == "latest": tagVer = self.latest()
        downUrl = "/".join([
            self.RELEASES_URL, "download", tagVer,
            f"die_win64_qt6_portable_{tagVer}.zip"])
        resp = HTTPGET(downUrl)
        if (200 == resp.status):
            return self.extract(resp.read(), os.path.basename(downUrl))

        raise Exception("download failed: " + downUrl)

    def extract(self, data=b'', target=''):
        import io, zipfile
        zipfile.ZipFile(io.BytesIO(data)).extractall()
        return os.getcwd()



if __name__ == "__main__":
    x64dbg().download()