#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, io, sys, re, pathlib, types, platform, subprocess, urllib.request

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


class gradle:
    ''' https://services.gradle.org/distributions/ '''
    GRADLE_VERSION = "8.5"

    def download(self, target_dir=".", tagVer="latest"):
        downUrl = f"https://services.gradle.org/distributions/gradle-{self.GRADLE_VERSION}-bin.zip"
        resp = HTTPGET(downUrl)
        if (200 == resp.status):
            return EXTRACT.zip(resp.read(), target_dir=target_dir)

        raise Exception("download failed: " + downUrl)

class openjdk:
    ''' https://repo.huaweicloud.com/openjdk/ '''
    ''' https://github.com/adoptium/temurin21-binaries/releases '''
    JDK_VERSION = 21

    class target:
        arch = dict({
            "i386": "x86-32", "i686": "x86-32", "x86": "x86-32",
            "amd64": "x64", "x86_64": "x64",
            "arm64": "aarch64",
        }).get(platform.machine().lower(), platform.machine().lower())

        system = dict({
            "darwin": "mac",
        }).get(platform.system().lower(), platform.system().lower())

    def download(self, target_dir=".", tagVer="latest"):
        downUrl = GITHUB_RELEASES(source=f"adoptium/temurin{self.JDK_VERSION}-binaries").geturl(
            f"OpenJDK\\d+U-jdk_{openjdk.target.arch}_{openjdk.target.system}_.*?.(tar.gz|zip)", tagVer)
        resp = HTTPGET(downUrl)
        if (200 == resp.status):
            return self.extract(resp.read(), target_dir=target_dir, target_name=os.path.basename(downUrl))

        raise Exception("download failed: " + downUrl)

    def extract(self, data, target_dir, target_name='OpenJDK.tar.gz'):
        if target_name.endswith("tar.gz"):
            EXTRACT.tar(data, target_dir=target_dir)
        elif target_name.endswith("zip"):
            EXTRACT.zip(data, target_dir=target_dir)

        target = next(f for f in os.listdir(target_dir) if f.startswith("jdk"))
        return os.path.join(os.getcwd(), target_dir, target)


class ghidra:
    ''' https://github.com/NationalSecurityAgency/ghidra/releases '''

    def download(self, target_dir="ghidra", tagVer="latest"):
        downUrl = GITHUB_RELEASES(source="NationalSecurityAgency/ghidra").geturl("ghidra_.*?_PUBLIC.*?.zip", tagVer)
        resp = HTTPGET(downUrl)
        if (200 == resp.status):
            return EXTRACT.zip(resp.read(), target_dir=target_dir) and \
                self.unixrun(target_dir) and self.winrun(target_dir)

        raise Exception("download failed: " + downUrl)

    def winrun(self, ghidra_dir):
        target = os.path.join(os.getcwd(), ghidra_dir)
        raw_lines = [
            f"@echo off",
            f"cd /D %~dp0",
            f"for /F %%i in ('dir /b jdk-{openjdk.JDK_VERSION}*') do (set \"JDK_INSTALL_DIR=%~dp0%%i\")",
            f"set \"JAVA_HOME=%JDK_INSTALL_DIR%\"",
            f"set \"PATH=%JAVA_HOME%\\bin;%PATH%\"",
            f"",
            f"for /F %%i in ('dir /b ghidra*') do (set \"GHIDRA_INSTALL_DIR=%~dp0%%i\")",
            f"cd \"%GHIDRA_INSTALL_DIR%\"",
            f"call ghidraRun.bat"
        ]
        with open(os.path.join(target, "ghidraRun.bat"), "w") as fp:
            [ print(l, file=fp) for l in raw_lines ]
        
        raw_lines[-1] = f"call support/pyghidraRun.bat"
        with open(os.path.join(target, "ghidraPyGhidra.bat"), "w") as fp:
            [ print(l, file=fp) for l in raw_lines ]

        return target

    def unixrun(self, ghidra_dir):
        target = os.path.join(os.getcwd(), ghidra_dir)
        raw_lines = [
            f"#!/usr/bin/env bash",
            f"cd \"$(dirname \"$0\")\"",
            f"export \"JDK_INSTALL_DIR=$(ls -d jdk-{openjdk.JDK_VERSION}*/)\"",
            "darwin" == platform.system().lower() and \
                f"export \"JAVA_HOME=$PWD/$JDK_INSTALL_DIR/Contents/Home\"" or 
                f"export \"JAVA_HOME=$PWD/$JDK_INSTALL_DIR\"",
            f"export \"PATH=$JAVA_HOME/bin:$PATH\"",
            f"",
            f"export \"GHIDRA_INSTALL_DIR=$(ls -d ghidra*/)\"",
            f"cd \"$GHIDRA_INSTALL_DIR\"",
            f"./ghidraRun"
        ]
        with open(os.path.join(target, "ghidraRun"), "w") as fp:
            [ print(l, file=fp) for l in raw_lines ]
        
        raw_lines[-1] = f"./support/pyghidraRun"
        with open(os.path.join(target, "ghidraPyGhidra"), "w") as fp:
            [ print(l, file=fp) for l in raw_lines ]
        
        if 'windows' != openjdk.target.system:
            subprocess.check_call(["chmod", "-R", "+x", os.path.dirname(target)])

        return target

    @staticmethod
    def plugin(ghidra_dir=''):
        def ghidra_version():
            tagVer = GITHUB_RELEASES(source="NationalSecurityAgency/ghidra").latest()
            return re.findall(r"Ghidra_([\d\.]+)_build", tagVer)[0]

        if not ghidra_dir:
            config = ("$APPDATA", "ghidra") \
                if ('windows' == platform.system().lower()) else ("~", ".config", "ghidra")
            lastrun = os.path.expanduser(
                os.path.join(
                    *config, "lastrun"))
            ghidra_dir = os.path.expanduser(
                os.path.join(
                    *config,
                    '_'.join(["ghidra", ghidra_version(), "PUBLIC"]), "Extensions"))
            os.makedirs(ghidra_dir, exist_ok=True)

        ''' ghidra plugin '''
        def BinExport(ghidra_dir):
            ''' https://github.com/google/bindiff/releases '''
            ''' https://github.com/google/binexport/releases '''
            downUrl = GITHUB_RELEASES(source="google/binexport").geturl("BinExport_Ghidra-Java.zip")
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir=ghidra_dir)

            raise Exception("download failed: " + downUrl)

        def Pyhidra(ghidra_dir):
            ''' https://github.com/dod-cyber-crime-center/pyhidra/releases/latest '''
            ''' https://github.com/NationalSecurityAgency/ghidra/tree/master/Ghidra/Features/PyGhidra/src/main/py '''

        def Ghidrathon(ghidra_dir):
            ''' https://github.com/mandiant/Ghidrathon/releases/latest '''

        def BTIGhidra(ghidra_dir):
            ''' https://github.com/trailofbits/BTIGhidra/releases/latest '''

        def GhidraEmu(ghidra_dir):
            ''' https://github.com/Nalen98/GhidraEmu/releases/latest '''

        def GolangAnalyzer(ghidra_dir):
            ''' https://github.com/mooncat-greenpy/Ghidra_GolangAnalyzerExtension/releases/latest '''

        def GhydraMCP(ghidra_dir):
            ''' https://github.com/starsong-consulting/GhydraMCP/releases/latest '''
            downUrl = GITHUB_RELEASES(source="starsong-consulting/GhydraMCP").geturl("GhydraMCP-v.*?.zip")
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir=ghidra_dir)

            raise Exception("download failed: " + downUrl)

        return \
            BinExport(ghidra_dir) \
            or GhydraMCP(ghidra_dir)



if __name__ == "__main__":

    os.makedirs(pathlib.Path.home() / "ghidra_scripts", exist_ok=True)

    GHIDRA = ghidra().download(target_dir='ghidra'); \
        openjdk().download(target_dir='ghidra', tagVer='jdk-21.0.6+7')

    ''' ghidra plugin '''