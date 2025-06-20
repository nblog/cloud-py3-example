#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, io, sys, re, types, platform, subprocess, urllib.request, zipfile

HTTPGET = urllib.request.urlopen

if not bool(os.environ.get("DEBUGPY_RUNNING")):
    source = "utils/common"
    RAW_CODE = HTTPGET(f"https://github.com/nblog/cloud-py3-example/blob/main/{source}.py?raw=true").read().decode('utf-8')

    raw_module = types.ModuleType(source.split('/')[-1])
    sys.modules[source.replace('/', '.')] = raw_module
    exec(RAW_CODE, raw_module.__dict__)

from utils.common import (
    EXTRACT, GITHUB_RELEASES
)


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
        '''  '''


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

    dnSpyEx().download(); \
        ILSpy().download()