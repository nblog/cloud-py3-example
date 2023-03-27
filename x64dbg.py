#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, platform, urllib.request, subprocess


HTTPGET = urllib.request.urlopen


class openjdk:

    JDK_VERSION = 17

    RELEASES_URL = os.environ.get("GHPROXY","") + \
        f"https://github.com/adoptium/temurin{JDK_VERSION}-binaries/releases"


    def latest(self):
        resp = HTTPGET( "/".join([self.RELEASES_URL, "latest"]) )
        tagVer = str(resp.url).split("tag/")[-1]
        return tagVer

    def download(self, tagVer="latest", target_dir=''):
        if tagVer == "latest": tagVer = self.latest()

        def assets(tagVer):
            import re
            resp = HTTPGET( "/".join([self.RELEASES_URL, "expanded_assets", tagVer]) )
            assets = re.findall(b">(OpenJDK\d+U-jdk_x64_windows_hotspot_[\w\x2e]+.zip)<", resp.read())[0].decode()
            return assets

        downUrl = "/".join([
            self.RELEASES_URL, "download", tagVer, assets(tagVer)])
        resp = HTTPGET(downUrl)
        if (200 == resp.status):
            return self.extract(resp.read(), target_dir)

        raise Exception("download failed: " + downUrl)

    def extract(self, data, target_dir):
        import io, zipfile
        zipfile.ZipFile(io.BytesIO(data)).extractall(target_dir)
        return os.path.join(os.getcwd(), target_dir)



class ghidra:

    RELEASES_URL = os.environ.get("GHPROXY","") + \
        "https://github.com/NationalSecurityAgency/ghidra/releases"


    def latest(self):
        resp = HTTPGET( "/".join([self.RELEASES_URL, "latest"]) )
        tagVer = str(resp.url).split("tag/")[-1]
        return tagVer

    def download(self, tagVer="latest", target_dir='ghidra'):
        if tagVer == "latest": tagVer = self.latest()

        def assets(tagVer):
            import re
            resp = HTTPGET( "/".join([ghidra.RELEASES_URL, "expanded_assets", tagVer]) )
            assets = re.findall(b">(ghidra_[0-9\x2e]+_PUBLIC_[0-9]+.zip)<", resp.read())[0].decode()
            return assets

        downUrl = "/".join([
            self.RELEASES_URL, "download", tagVer, assets(tagVer)])
        resp = HTTPGET(downUrl)
        if (200 == resp.status):
            return self.extract(resp.read(), target_dir) and \
                openjdk().download(target_dir=target_dir) and \
                open(os.path.join(target_dir, "ghidraRun.bat"), "w").write(
                    f"@echo off\r\ncd /d %~dp0\r\n"
                    f"for /F %%i in ('dir /b jdk-{openjdk.JDK_VERSION}*') do (set JDK_DIR=%%i)\r\n"
                    f"for /F %%i in ('dir /b ghidra*') do (set GHIDRA_DIR=%%i)\r\n"
                    f"set JAVA_HOME=%~dp0%JDK_DIR%\r\n"
                    f"set PATH=%JAVA_HOME%\\bin;%PATH%\r\n"
                    f"call \"%~dp0%GHIDRA_DIR%\ghidraRun.bat\"\r\n"
                )

        raise Exception("download failed: " + downUrl)

    def extract(self, data, target_dir):
        import io, zipfile
        zipfile.ZipFile(io.BytesIO(data)).extractall(target_dir)
        return os.path.join(os.getcwd(), target_dir)



class x64dbg:

    RELEASES_URL = os.environ.get("GHPROXY","") + \
        "https://github.com/x64dbg/x64dbg/releases"


    def latest(self):
        resp = HTTPGET( "/".join([self.RELEASES_URL, "latest"]) )
        tagVer = str(resp.url).split("tag/")[-1]
        return tagVer

    def download(self, tagVer="latest", target_dir='x64dbg'):
        if tagVer == "latest": tagVer = self.latest()

        def assets(tagVer):
            import re
            resp = HTTPGET( "/".join([x64dbg.RELEASES_URL, "expanded_assets", tagVer]) )
            assets = re.findall(b">(snapshot[0-9\x2d\x5f]+.zip)<", resp.read())[0].decode()
            return assets

        downUrl = "/".join([
            self.RELEASES_URL, "download", tagVer, assets(tagVer)])
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

    def download(self, tagVer="latest", target_dir=''):
        if tagVer == "latest": tagVer = self.latest()
        downUrl = "/".join([
            self.RELEASES_URL, "download", tagVer,
            f"die_win64_qt6_portable_{tagVer}.zip"])
        resp = HTTPGET(downUrl)
        if (200 == resp.status):
            target_dir = os.path.splitext(os.path.basename(downUrl))[0]
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

    def download(self, tagVer="latest", target_dir=''):
        if tagVer == "latest": tagVer = self.latest()
        downUrl = "/".join([
            self.RELEASES_URL, "download", tagVer,
            f"upx-{tagVer[1:]}-win64.zip"])
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

    def download(self, tagVer="latest", target_dir=''):
        if tagVer == "latest": tagVer = self.latest()
        downUrl = "/".join([
            self.RELEASES_URL, "download", tagVer,
            f"DB.Browser.for.SQLite-{tagVer[1:]}-win64.zip"])
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


if __name__ == "__main__":

    x64dbg().download()

    die_engine().download()

    sysinternals.debugview().download()