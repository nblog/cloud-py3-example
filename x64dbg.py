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
            return self.extract(resp.read(), "x64dbg")

        raise Exception("download failed: " + downUrl)

    def extract(self, data=b'', target_dir=''):
        import io, zipfile
        zipfile.ZipFile(io.BytesIO(data)).extractall(target_dir)
        return os.path.join(os.getcwd(), target_dir)

    def plugin(self):
        ''' x64dbg plugin '''
        '''
        https://down.52pojie.cn/Tools/OllyDbg_Plugin/SharpOD_x64_v0.6d_Stable.zip
        https://github.com/codecat/ClawSearch/releases/latest
        '''
        raise NotImplementedError


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
            return self.extract(resp.read(), os.path.splitext(os.path.basename(downUrl))[0])

        raise Exception("download failed: " + downUrl)

    def extract(self, data=b'', target_dir=''):
        import io, zipfile
        zipfile.ZipFile(io.BytesIO(data)).extractall(target_dir)
        return os.path.join(os.getcwd(), target_dir)


class sysinternals:

    class debugview:
        def download(self):
            downUrl = "https://download.sysinternals.com/files/DebugView.zip"
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return self.extract(resp.read(), os.path.join("sysinternals", "debugview"))

        def extract(self, data=b'', target_dir=''):
            import io, zipfile
            zipfile.ZipFile(io.BytesIO(data)).extractall(target_dir)
            return os.path.join(os.getcwd(), target_dir)



if __name__ == "__main__":
    x64dbg().download()

    die_engine().download()

    sysinternals.debugview().download()