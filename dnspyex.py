#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, io, sys, re, platform, urllib.request, zipfile, tarfile


HTTPGET = urllib.request.urlopen


class EXTRACT:

    @staticmethod
    def zip(data, target_dir, zipfilter=None):
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            for member in filter(zipfilter, archive.infolist()):
                archive.extract(member, target_dir)
        return os.path.join(os.getcwd(), target_dir)

    @staticmethod
    def tar(data, target_dir):
        tarfile.open(fileobj=io.BytesIO(data)).extractall(target_dir)
        return os.path.join(os.getcwd(), target_dir)

    @staticmethod
    def bin(data, target_dir, target_name):
        target = os.path.join(target_dir, target_name)
        os.makedirs(target_dir, exist_ok=True)
        open(target, "wb").write(data)
        return target


class GITHUB_RELEASES:
    def __init__(self, source=None, author=None, project=None):
        if (None == source) and (None == author or None == project):
            raise Exception("author and project must be specified")
        self.RELEASES_URL = f"https://github.com/{author}/{project}/releases" \
            if None == source else f"https://github.com/{str.split(source, '/')[0]}/{str.split(source, '/')[1]}/releases"
    def latest(self):
        resp = HTTPGET( "/".join([self.RELEASES_URL, "latest"]) )
        tagVer = str(resp.url).split("tag/")[-1]
        return tagVer
    def assets(self, tagVer):
        if "latest" == tagVer: tagVer = self.latest()
        resp = HTTPGET( "/".join([self.RELEASES_URL, "expanded_assets", tagVer]) )
        return re.findall("<a href=\"(.*?)\"", resp.read().decode())
    def geturl(self, re_pattern="\.zip", tagVer="latest"):
        target = list(filter(lambda href: re.search(re_pattern, href), self.assets(tagVer)))[0]
        return f"https://github.com/{target}"



class misc:

    class GarbageMan:
        ''' https://github.com/WithSecureLabs/GarbageMan/releases '''
        def download(self, target_dir="GarbageMan", tagVer="latest"):
            downUrl = GITHUB_RELEASES(source="WithSecureLabs/GarbageMan").geturl("GarbageMan.*?\.zip", tagVer)
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir=target_dir)

            raise Exception("download failed: " + downUrl)

    class UAssetGUI:
        ''' https://github.com/atenfyr/UAssetGUI/releases '''

    class UnityExplorer:
        ''' https://github.com/yukieiji/UnityExplorer/releases '''

    class ExtremeDumper:
        ''' https://github.com/wwh1004/ExtremeDumper/releases '''


class dnSpyEx:
    ''' https://github.com/dnSpyEx/dnSpy/releases '''
    def download(self, target_dir="dnSpy", tagVer="latest"):
        downUrl = GITHUB_RELEASES(source="dnSpyEx/dnSpy").geturl("dnSpy-netframework.*?.zip", tagVer)
        resp = HTTPGET(downUrl)
        if (200 == resp.status):
            return EXTRACT.zip(resp.read(), target_dir=target_dir)

        raise Exception("download failed: " + downUrl)

    class plugins:
        class cpp2il:
            ''' https://github.com/BadRyuner/dnspy.Cpp2IL/releases '''


class ILSpy:
    ''' https://github.com/icsharpcode/ILSpy/releases '''
    def download(self, target_dir="ILSpy", tagVer="latest"):
        downUrl = GITHUB_RELEASES(source="icsharpcode/ILSpy").geturl("ILSpy_selfcontained_.*?\.zip", tagVer)
        resp = HTTPGET(downUrl)
        if (200 == resp.status):
            return EXTRACT.zip(resp.read(), target_dir=target_dir)

        raise Exception("download failed: " + downUrl)


class metadata:

    class win32metadata:
        ''' https://github.com/microsoft/win32metadata/releases '''
        def download(self, target_dir="win32metadata", tagVer="latest"):
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
        ''' https://github.com/microsoft/wdkmetadata/releases '''
        def download(self, target_dir="wdkmetadata", tagVer="latest"):
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