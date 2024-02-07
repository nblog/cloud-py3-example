#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, re, platform, urllib.request, subprocess


HTTPGET = urllib.request.urlopen


class openjdk:

    JDK_VERSION = 17

    ''' https://repo.huaweicloud.com/openjdk/ '''
    RELEASES_URL = f"https://github.com/adoptium/temurin{JDK_VERSION}-binaries/releases"

    class TARGET:
        arch = dict({
            "i386": "x86-32", "i686": "x86-32", "x86": "x86-32",
            "amd64": "x64", "x86_64": "x64",
        }).get(platform.machine().lower(), platform.machine().lower())

        system = dict({
            "darwin": "mac",
        }).get(platform.system().lower(), platform.system().lower())


    def latest(self):
        resp = HTTPGET( "/".join([self.RELEASES_URL, "latest"]) )
        tagVer = str(resp.url).split("tag/")[-1]
        return tagVer

    def assets(self, tagVer, system=TARGET):
        resp = HTTPGET( "/".join([self.RELEASES_URL, "expanded_assets", tagVer]) )
        assets = re.findall(f">(OpenJDK\d+U-jdk_{system.arch}_{system.system}.*?)<", resp.read().decode())
        return assets

    def download(self, tagVer="latest", target_dir='.'):
        if tagVer == "latest": tagVer = self.latest()
        target = [asset for asset in self.assets(tagVer) \
                  if asset.endswith(".tar.gz") or asset.endswith(".zip")][0]
        downUrl = "/".join([
            self.RELEASES_URL, "download", tagVer, target])
        resp = HTTPGET(downUrl)
        if (200 == resp.status):
            return self.extract(resp.read(), target, target_dir)

        raise Exception("download failed: " + downUrl)

    def extract(self, data, target, target_dir):
        import io, zipfile, tarfile
        if target.endswith("tar.gz"):
            tarfile.open(fileobj=io.BytesIO(data)).extractall(target_dir)
        elif target.endswith("zip"):
            zipfile.ZipFile(io.BytesIO(data)).extractall(target_dir)

        target = [f for f in os.listdir(target_dir) if f.startswith("jdk")][0]
        return os.path.join(os.getcwd(), target_dir, target)


class ghidra:

    RELEASES_URL = "https://github.com/NationalSecurityAgency/ghidra/releases"

    def latest(self):
        resp = HTTPGET( "/".join([self.RELEASES_URL, "latest"]) )
        tagVer = str(resp.url).split("tag/")[-1]
        return tagVer

    def assets(self, tagVer):
        resp = HTTPGET( "/".join([self.RELEASES_URL, "expanded_assets", tagVer]) )
        assets = re.findall(">(ghidra_.*?.zip)<", resp.read().decode())
        return assets

    def download(self, tagVer="latest", target_dir='ghidra'):
        if tagVer == "latest": tagVer = self.latest()
        target = self.assets(tagVer)[0]
        downUrl = "/".join([self.RELEASES_URL, "download", tagVer, target])
        resp = HTTPGET(downUrl)
        if (200 == resp.status):
            return self.extract(resp.read(), target_dir) and \
                self.winrun(target_dir)

        raise Exception("download failed: " + downUrl)

    def extract(self, data, target_dir):
        import io, zipfile
        zipfile.ZipFile(io.BytesIO(data)).extractall(target_dir)
        return os.path.join(os.getcwd(), target_dir)

    def winrun(self, ghidra_dir):
        target = os.path.join(os.getcwd(), ghidra_dir, "ghidraRun.bat")
        raw_lines = [
            f"@echo off",
            f"cd /D %~dp0",
            f"for /F %%i in ('dir /b jdk-{openjdk.JDK_VERSION}*') do (set JDK_INSTALL_DIR=%~dp0%%i)",
            f"for /F %%i in ('dir /b ghidra*') do (set GHIDRA_INSTALL_DIR=%~dp0%%i)",
            f"set JAVA_HOME=%JDK_INSTALL_DIR%",
            f"set PATH=%JAVA_HOME%\\bin;%PATH%",
            f"cd \"%GHIDRA_INSTALL_DIR%\" && call ghidraRun.bat"]
        with open(target, "w") as fp:
            [ print(l, file=fp) for l in raw_lines ]
        return target

    @staticmethod
    def plugin(ghidra_dir=''):
        def ghidra_version():
            tagVer = ghidra.latest(ghidra)
            return re.findall("Ghidra_([\d\.]+)_build", tagVer)[0]

        if not ghidra_dir:
            ghidra_dir = os.path.expanduser(
                os.path.join(
                "~", 
                ".ghidra", 
                '_'.join([".ghidra", ghidra_version(), "PUBLIC"]), "Extensions"))

        ''' ghidra plugin '''
        def GhidraPyi(ghidra_dir):
            ''' https://github.com/VDOO-Connected-Trust/ghidra-pyi-generator/releases/latest '''

        def Ghidrathon(ghidra_dir):
            ''' https://github.com/mandiant/Ghidrathon/releases/latest '''

        def Pyhidra(ghidra_dir):
            ''' https://github.com/dod-cyber-crime-center/pyhidra/releases/latest '''
            raise NotImplementedError

        def BinExport(ghidra_dir):
            ''' https://github.com/google/binexport/releases '''
            ''' https://github.com/google/bindiff/releases '''

        def BTIGhidra(ghidra_dir):
            ''' https://github.com/trailofbits/BTIGhidra '''

        def GhidraEmu(ghidra_dir):
            ''' https://github.com/Nalen98/GhidraEmu/releases/latest '''

        return \
            GhidraEmu(ghidra_dir) \
            or BinExport(ghidra_dir)



if __name__ == "__main__":

    GHIDRA = ghidra().download(); \
        openjdk().download(target_dir='ghidra')
