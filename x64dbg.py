#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, re, platform, urllib.request, subprocess


HTTPGET = urllib.request.urlopen


class x64dbg:

    RELEASES_URL = os.environ.get("GHPROXY","") + \
        "https://github.com/x64dbg/x64dbg/releases"


    def latest(self):
        resp = HTTPGET( "/".join([self.RELEASES_URL, "latest"]) )
        tagVer = str(resp.url).split("tag/")[-1]
        return tagVer

    def assets(self, tagVer):
        resp = HTTPGET( "/".join([self.RELEASES_URL, "expanded_assets", tagVer]) )
        assets = re.findall(">(snapshot_.*?.zip)<", resp.read().decode())
        return assets

    def download(self, tagVer="latest", target_dir='x64dbg'):
        if tagVer == "latest": tagVer = self.latest()
        target = self.assets(tagVer)[0]
        downUrl = "/".join([self.RELEASES_URL, "download", tagVer, target])
        resp = HTTPGET(downUrl)
        if (200 == resp.status):
            return self.extract(resp.read(), target_dir)

        raise Exception("download failed: " + downUrl)

    def extract(self, data, target_dir):
        import io, zipfile
        zipfile.ZipFile(io.BytesIO(data)).extractall(target_dir)
        return os.path.join(os.getcwd(), target_dir)

    def plugin(self):
        ''' x64dbg plugin '''
        '''
        https://down.52pojie.cn/Tools/OllyDbg_Plugin/SharpOD_x64_v0.6d_Stable.zip
        https://github.com/fjqisba/E-Debug/releases

        https://ramensoftware.com/downloads/multiasm.rar
        https://github.com/codecat/ClawSearch/releases/latest
        '''
        raise NotImplementedError



class die_engine:

    RELEASES_URL = os.environ.get("GHPROXY","") + \
        "https://github.com/horsicq/DIE-engine/releases"


    def latest(self):
        resp = HTTPGET( "/".join([self.RELEASES_URL, "latest"]) )
        tagVer = str(resp.url).split("tag/")[-1]
        return tagVer

    def assets(self, tagVer):
        resp = HTTPGET( "/".join([self.RELEASES_URL, "expanded_assets", tagVer]) )
        assets = re.findall(f">(die_win64_portable_{tagVer}?.zip)<", resp.read().decode())
        return assets

    def download(self, tagVer="latest", target_dir='.'):
        if tagVer == "latest": tagVer = self.latest()
        target = self.assets(tagVer)[0]
        downUrl = "/".join([self.RELEASES_URL, "download", tagVer, target])
        resp = HTTPGET(downUrl)
        if (200 == resp.status):
            target_dir = os.path.splitext(target)[0]
            return self.extract(resp.read(), target_dir)

        raise Exception("download failed: " + downUrl)

    def extract(self, data, target_dir):
        import io, zipfile
        zipfile.ZipFile(io.BytesIO(data)).extractall(target_dir)
        return os.path.join(os.getcwd(), target_dir)



class upx:

    RELEASES_URL = os.environ.get("GHPROXY","") + \
        "https://github.com/upx/upx/releases"


    def latest(self):
        resp = HTTPGET( "/".join([self.RELEASES_URL, "latest"]) )
        tagVer = str(resp.url).split("tag/")[-1]
        return tagVer

    def assets(self, tagVer):
        resp = HTTPGET( "/".join([self.RELEASES_URL, "expanded_assets", tagVer]) )
        assets = re.findall(">(upx-.*?-win64.zip)<", resp.read().decode())
        return assets

    def download(self, tagVer="latest", target_dir='.'):
        if tagVer == "latest": tagVer = self.latest()
        target = self.assets(tagVer)[0]
        downUrl = "/".join([self.RELEASES_URL, "download", tagVer, target])
        resp = HTTPGET(downUrl)
        if (200 == resp.status):
            return self.extract(resp.read(), target_dir)

        raise Exception("download failed: " + downUrl)

    def extract(self, data, target_dir):
        import io, zipfile
        zipfile.ZipFile(io.BytesIO(data)).extractall(target_dir)
        return os.path.join(os.getcwd(), target_dir)



class sqlitebrowser:

    RELEASES_URL = os.environ.get("GHPROXY","") + \
        "https://github.com/sqlitebrowser/sqlitebrowser/releases"


    def latest(self):
        resp = HTTPGET( "/".join([self.RELEASES_URL, "latest"]) )
        tagVer = str(resp.url).split("tag/")[-1]
        return tagVer

    def assets(self, tagVer):
        resp = HTTPGET( "/".join([self.RELEASES_URL, "expanded_assets", tagVer]) )
        assets = re.findall(">(DB.Browser.for.SQLite-.*?-win64.zip)<", resp.read().decode())
        return assets

    def download(self, tagVer="latest", target_dir='.'):
        if tagVer == "latest": tagVer = self.latest()
        target = self.assets(tagVer)[0]
        downUrl = "/".join([self.RELEASES_URL, "download", tagVer, target])
        resp = HTTPGET(downUrl)
        if (200 == resp.status):
            return self.extract(resp.read(), target_dir)

        raise Exception("download failed: " + downUrl)

    def extract(self, data, target_dir):
        import io, zipfile
        zipfile.ZipFile(io.BytesIO(data)).extractall(target_dir)
        return os.path.join(os.getcwd(), target_dir)



class sysinternals:

    class debugview:
        def download(self, target_dir='debugview'):
            downUrl = "https://download.sysinternals.com/files/DebugView.zip"
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return self.extract(resp.read(), os.path.join("sysinternals", target_dir))

        def extract(self, data, target_dir):
            import io, zipfile
            zipfile.ZipFile(io.BytesIO(data)).extractall(target_dir)
            return os.path.join(os.getcwd(), target_dir)



class resourcehacker:
    def download(self, target_dir='resourcehacker'):
        downUrl = "http://angusj.com/resourcehacker/resource_hacker.zip"
        resp = HTTPGET(downUrl)
        if (200 == resp.status):
            return self.extract(resp.read(), target_dir)

    def extract(self, data, target_dir):
        import io, zipfile
        zipfile.ZipFile(io.BytesIO(data)).extractall(target_dir)
        return os.path.join(os.getcwd(), target_dir)



class winark:
    ''' Windows Anti-Rootkit '''

    @staticmethod
    def extract(data, target_dir):
        import io, zipfile
        zipfile.ZipFile(io.BytesIO(data)).extractall(target_dir)
        return os.path.join(os.getcwd(), target_dir)

    class WKE:
        def download(self, target_dir='ark'):
            downUrl = os.environ.get("GHPROXY","") + \
                "https://github.com/AxtMueller/Windows-Kernel-Explorer" \
                "/archive/refs/heads/master.zip"
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return winark.extract(resp.read(), target_dir)

    class WKTools:
        def download(self, target_dir='ark'):
            downUrl = os.environ.get("GHPROXY","") + \
                "https://github.com/AngleHony/WKTools" \
                "/archive/refs/heads/main.zip"
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return winark.extract(resp.read(), target_dir)



if __name__ == "__main__":

    x64dbg().download()

    sysinternals.debugview().download()


    winark.WKE().download(); winark.WKTools().download()
