#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, re, platform, urllib.request


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



class misc:

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

    class UAssetGUI:

        RELEASES_URL = "https://github.com/atenfyr/UAssetGUI/releases"

    class UnityExplorer:

        RELEASES_URL = "https://github.com/yukieiji/UnityExplorer/releases"

    class ExtremeDumper:

        RELEASES_URL = "https://github.com/wwh1004/ExtremeDumper/releases"



class dnSpyEx:

    class plugins:
        class cpp2il:
            RELEASES_URL = "https://github.com/BadRyuner/dnspy.Cpp2IL/releases"

    RELEASES_URL = "https://github.com/dnSpyEx/dnSpy/releases"

    def latest(self):
        resp = HTTPGET( "/".join([self.RELEASES_URL, "latest"]) )
        tagVer = str(resp.url).split("tag/")[-1]
        return tagVer

    def assets(self, tagVer):
        resp = HTTPGET( "/".join([self.RELEASES_URL, "expanded_assets", tagVer]) )
        assets = re.findall(">(dnSpy-netframework.zip)<", resp.read().decode())
        return assets

    def download(self, tagVer="latest", target_dir='dnSpy'):
        if tagVer == "latest": tagVer = self.latest()

        target = self.assets(tagVer)[0]
        downUrl = "/".join([self.RELEASES_URL, "download", tagVer, target])
        resp = HTTPGET(downUrl)
        if (200 == resp.status):
            return EXTRACT.zip(resp.read(), target_dir=os.path.join( \
                target_dir, os.path.splitext(os.path.basename(target))[0]))

        raise Exception("download failed: " + downUrl)


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


class metadata:

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
                return False

            downUrl = \
                "https://www.nuget.org/api/v2/package/" \
                    "{}/{}".format("Microsoft.Windows.SDK.Win32Metadata", tagVer[1:])
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(
                    resp.read(), target_dir=target_dir, zipfilter=zipfilter)

            raise Exception("download failed: " + downUrl)

    class wdkmetadata:

        RELEASES_URL = "https://github.com/microsoft/wdkmetadata/releases"

        def latest(self):
            resp = HTTPGET( "/".join([self.RELEASES_URL, "latest"]) )
            tagVer = str(resp.url).split("tag/")[-1]
            return tagVer

        def download(self, tagVer="latest", target_dir='wdkmetadata'):
            if tagVer == "latest": tagVer = self.latest()

            import zipfile
            def zipfilter(m:zipfile.ZipInfo):
                if (m.filename.lower() == "windows.wdk.winmd"):
                    return True
                return False

            downUrl = \
                "https://www.nuget.org/api/v2/package/" \
                    "{}/{}".format("Microsoft.Windows.WDK.Win32Metadata", tagVer[1:])
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(
                    resp.read(), target_dir=target_dir, zipfilter=zipfilter)

            raise Exception("download failed: " + downUrl)



if __name__ == "__main__":

    if 'windows' != platform.system().lower():
        raise NotImplementedError("only support windows")

    dnSpyEx().download()