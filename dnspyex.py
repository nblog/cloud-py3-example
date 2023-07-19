#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, re, platform, urllib.request, subprocess


HTTPGET = urllib.request.urlopen


class EXTRACT:

    @staticmethod
    def zip(data, target_dir, zipfilter=None):
        import io, zipfile
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            for member in filter(zipfilter, archive.infolist()):
                archive.extract(member, target_dir)
        return os.path.join(os.getcwd(), target_dir)

    @staticmethod
    def tar(data, target_dir):
        import io, tarfile
        tarfile.open(fileobj=io.BytesIO(data)).extractall(target_dir)
        return os.path.join(os.getcwd(), target_dir)

    @staticmethod
    def binary(data, target_dir, target_name):
        target = os.path.join(target_dir, target_name)
        os.makedirs(target_dir, exist_ok=True)
        open(target, "wb").write(data)
        return target



class dumper:

    class ExtremeDumper:
        ''' https://github.com/wwh1004/ExtremeDumper '''


class dnSpyEx:

    RELEASES_URL = "https://github.com/dnSpyEx/dnSpy/releases"


    def latest(self):
        resp = HTTPGET( "/".join([self.RELEASES_URL, "latest"]) )
        tagVer = str(resp.url).split("tag/")[-1]
        return tagVer

    def assets(self, tagVer):
        resp = HTTPGET( "/".join([self.RELEASES_URL, "expanded_assets", tagVer]) )
        assets = re.findall(">(dnSpy-net-.*?.zip)<", resp.read().decode())
        return assets

    def download(self, tagVer="latest", target_dir='dnSpy'):
        if tagVer == "latest": tagVer = self.latest()

        succeed = ''
        for target in self.assets(tagVer):
            downUrl = "/".join([self.RELEASES_URL, "download", tagVer, target])
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                succeed = EXTRACT.zip(resp.read(), target_dir=os.path.join( \
                    target_dir, os.path.splitext(os.path.basename(target))[0]))

                if (not succeed): raise Exception("download failed: " + downUrl)

        return succeed


class ILSpy:

    RELEASES_URL = "https://github.com/icsharpcode/ILSpy/releases"


    def latest(self):
        resp = HTTPGET( "/".join([self.RELEASES_URL, "latest"]) )
        tagVer = str(resp.url).split("tag/")[-1]
        return tagVer

    def assets(self, tagVer):
        resp = HTTPGET( "/".join([self.RELEASES_URL, "expanded_assets", tagVer]) )
        assets = re.findall(">(ILSpy_selfcontained.*?.zip)<", resp.read().decode())
        return assets

    def download(self, tagVer="latest", target_dir='ILSpy'):
        if tagVer == "latest": tagVer = self.latest()

        target = self.assets(tagVer)[0]
        downUrl = "/".join([self.RELEASES_URL, "download", tagVer, target])
        resp = HTTPGET(downUrl)
        if (200 == resp.status):
            return EXTRACT.zip(resp.read(), target_dir=os.path.join( \
                target_dir, os.path.splitext(os.path.basename(target))[0]))

        raise Exception("download failed: " + downUrl)


class ReClassNET:

    RELEASES_URL = "https://github.com/ReClassNET/ReClass.NET/releases"


    def latest(self):
        resp = HTTPGET( "/".join([self.RELEASES_URL, "latest"]) )
        tagVer = str(resp.url).split("tag/")[-1]
        return tagVer

    def assets(self, tagVer):
        resp = HTTPGET( "/".join([self.RELEASES_URL, "expanded_assets", tagVer]) )
        assets = re.findall(">(ReClass.NET.*?.rar)<", resp.read().decode())
        return assets

    def download(self, tagVer="latest", target_dir='ReClassNET'):
        if tagVer == "latest": tagVer = self.latest()

        target = self.assets(tagVer)[0]
        downUrl = "/".join([self.RELEASES_URL, "download", tagVer, target])
        resp = HTTPGET(downUrl)
        if (200 == resp.status):
            raise NotImplementedError("rar file not support yet")
            return EXTRACT.zip(resp.read(), target_dir=os.path.join( \
                target_dir, os.path.splitext(os.path.basename(target))[0]))

        raise Exception("download failed: " + downUrl)


class GarbageMan:

    RELEASES_URL = "https://github.com/WithSecureLabs/GarbageMan/releases"

    def latest(self):
        resp = HTTPGET( "/".join([self.RELEASES_URL, "latest"]) )
        tagVer = str(resp.url).split("tag/")[-1]
        return tagVer

    def assets(self, tagVer):
        resp = HTTPGET( "/".join([self.RELEASES_URL, "expanded_assets", tagVer]) )
        assets = re.findall(">(GarbageMan.*?.zip)<", resp.read().decode())
        return assets

    def download(self, tagVer="latest", target_dir='GarbageMan'):
        raise NotImplementedError("not support yet")



class win32metadata:

    RELEASES_URL = "https://github.com/microsoft/win32metadata/releases"

    def latest(self):
        resp = HTTPGET( "/".join([self.RELEASES_URL, "latest"]) )
        tagVer = str(resp.url).split("tag/")[-1]
        return tagVer

    def download(self, tagVer="latest", target_dir='win32metadata'):
        if tagVer == "latest": tagVer = self.latest()

        import zipfile
        def zipfilter(m:zipfile.ZipInfo):
            if (m.filename.lower() == "windows.win32.winmd"):
                return True
            else:
                return False

        downUrl = \
            "https://www.nuget.org/api/v2/package" \
                "/Microsoft.Windows.SDK.Win32Metadata/{0}".format(tagVer[1:])
        resp = HTTPGET(downUrl)
        if (200 == resp.status):
            return EXTRACT.zip(
                resp.read(), target_dir=target_dir, zipfilter=zipfilter)

        raise Exception("download failed: " + downUrl)



if __name__ == "__main__":

    if 'windows' != platform.system().lower():
        raise NotImplementedError("only support windows")

    dnSpyEx().download()