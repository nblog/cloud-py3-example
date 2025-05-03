#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, io, sys, re, types, platform, subprocess, urllib.request, zipfile

HTTPGET = urllib.request.urlopen

if not "DEBUGPY_RUNNING" in os.environ:
    target = "utils/common"
    RAW_CODE = HTTPGET(f"https://github.com/nblog/cloud-py3-example/blob/main/{target}.py?raw=true").read().decode('utf-8')

    raw_module = types.ModuleType(os.path.basename(target))
    sys.modules[target.replace('/', '.')] = raw_module
    exec(RAW_CODE, raw_module.__dict__)

from utils.common import (
    EXTRACT, GITHUB_RELEASES
)


class dumper:

    class binskim:
        ''' https://github.com/microsoft/binskim/releases '''
        def download(self, target_dir="binskim", tagVer="latest"):
            def zipfilter(m:zipfile.ZipInfo):
                if (re.match(r"^tools/netcoreapp3.1/win", m.filename)):
                    m.filename = re.sub(r"^tools/netcoreapp3.1/win", "", m.filename)
                    return True
                return False

            downUrl = \
                "https://www.nuget.org/api/v2/package/" \
                    "{}/{}".format("Microsoft.CodeAnalysis.BinSkim", tagVer[1:])
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(
                    resp.read(), target_dir=target_dir, zipfilter=zipfilter)

            raise Exception("download failed: " + downUrl)

    class winchecksec:
        ''' https://github.com/trailofbits/winchecksec/releases '''
        def download(self, target_dir="winchecksec", tagVer="latest"):
            def zipfilter(m:zipfile.ZipInfo):
                if (re.match(r"^build/Release", m.filename)):
                    m.filename = re.sub(r"^build/Release", "", m.filename)
                    return True
                return False

            downUrl = GITHUB_RELEASES(source="trailofbits/winchecksec").geturl("windows\.x64\.Release\.zip", tagVer)
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir=target_dir, zipfilter=zipfilter)

            raise Exception("download failed: " + downUrl)

    class ksdumper:
        ''' https://github.com/mastercodeon314/KsDumper-11/releases '''
        def download(self, target_dir="ksdumper", tagVer="latest"):
            downUrl = GITHUB_RELEASES(source="mastercodeon314/KsDumper-11").geturl("KsDumper11.*?\.zip", tagVer)
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir=target_dir)

            raise Exception("download failed: " + downUrl)

    class hollowshunter:
        ''' https://github.com/hasherezade/hollows_hunter '''
        def download(self, target_dir="hollowshunter", tagVer="latest"):
            downUrl = GITHUB_RELEASES(source="hasherezade/hollows_hunter").geturl("hollows_hunter64\.zip", tagVer)
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir=target_dir)

            raise Exception("download failed: " + downUrl)

    class oleviewdotnet:
        ''' https://github.com/tyranid/oleviewdotnet/releases '''

    class ReClassNET:
        ''' https://github.com/ReClassNET/ReClass.NET/releases '''
        def download(self, target_dir="ReClassNET", tagVer="latest"):
            downUrl = GITHUB_RELEASES(source="ReClassNET/ReClass.NET").geturl("ReClass.NET.*?\.rar", tagVer)
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                raise NotImplementedError("rar file not support yet")

            raise Exception("download failed: " + downUrl)


class debugger:

    class x64dbg:
        ''' https://github.com/x64dbg/x64dbg/releases '''
        def download(self, target_dir="x64dbg", tagVer="latest"):
            downUrl = GITHUB_RELEASES(source="x64dbg/x64dbg").geturl("snapshot_.*?\.zip", tagVer)
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir=target_dir)

            raise Exception("download failed: " + downUrl)

        @staticmethod
        def plugin(target_dir):
            ''' x64dbg plugin '''
            def ScyllaHide(target_dir):
                ''' https://github.com/x64dbg/ScyllaHide/releases '''

            def TitanHide(target_dir):
                ''' https://github.com/mrexodia/TitanHide/releases '''

            def OllyDumpEx(target_dir):
                ''' https://low-priority.appspot.com/ollydumpex/OllyDumpEx.zip '''

            def SharpOD(target_dir):
                def zipfilter(m:zipfile.ZipInfo):
                    if (re.match(r"^SharpOD_x64_v0.6d Stable/x64dbg", m.filename)):
                        m.filename = re.sub(r"^SharpOD_x64_v0.6d Stable/x64dbg", "", m.filename)
                        return True
                    return False

                resp = HTTPGET(
                    "https://down.52pojie.cn/Tools/OllyDbg_Plugin/SharpOD_x64_v0.6d_Stable.zip")
                if (200 == resp.status):
                    return EXTRACT.zip(resp.read(), target_dir=os.path.join(target_dir, "release"), zipfilter=zipfilter)

            return \
                ScyllaHide(target_dir) \
                    or TitanHide(target_dir) \
                    or SharpOD(target_dir)

    class cutter:
        ''' https://github.com/rizinorg/cutter/releases '''
        def download(self, target_dir="cutter", tagVer="latest"):
            downUrl = GITHUB_RELEASES(source="rizinorg/cutter").geturl("Cutter.*?\.zip", tagVer)
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir='.')

            raise Exception("download failed: " + downUrl)


class sysinternals:
    ''' https://download.sysinternals.com/files/SysinternalsSuite.zip '''
    ''' https://download.sysinternals.com/files/SysinternalsSuite-ARM64.zip '''

    class ZoomIt:
        def download(self, target_dir="zoomit"):
            downUrl = "https://download.sysinternals.com/files/ZoomIt.zip"
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir=target_dir)

            raise Exception("download failed: " + downUrl)

    class Testlimit:
        def download(self, target_dir="sysinternals/testlimit"):
            downUrl = "https://download.sysinternals.com/files/Testlimit.zip"
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir=target_dir)

            raise Exception("download failed: " + downUrl)

    class DebugView:
        def download(self, target_dir="sysinternals/debugview"):
            downUrl = "https://download.sysinternals.com/files/DebugView.zip"
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir=target_dir)

    class ProcessExplorer:
        def download(self, target_dir="sysinternals/procexp"):
            downUrl = "https://download.sysinternals.com/files/ProcessExplorer.zip"
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir=target_dir)

    class PSTools:
        def download(self, target_dir="sysinternals/pstools"):
            downUrl = "https://download.sysinternals.com/files/PSTools.zip"
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir=target_dir)

    class WinObj:
        def download(self, target_dir="sysinternals/winobj"):
            downUrl = "https://download.sysinternals.com/files/WinObj.zip"
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir=target_dir)

    class Sysmon:
        ''' https://github.com/microsoft/SysmonForLinux/releases '''
        def download(self, target_dir="sysinternals/sysmon", tagVer="latest"):
            if "linux" == platform.system().lower():
                downUrl = GITHUB_RELEASES(source="Sysinternals/SysmonForLinux").geturl("sysmonforlinux.*?\.tar\.gz", tagVer)
                resp = HTTPGET(downUrl)
                raise NotImplementedError("linux sysmon not implemented")
            else:
                downUrl = "https://download.sysinternals.com/files/Sysmon.zip"
                resp = HTTPGET(downUrl)
                if (200 == resp.status):
                    return EXTRACT.zip(resp.read(), target_dir=target_dir)

            raise Exception("download failed: " + downUrl)

    class ProcessMonitor:
        ''' https://github.com/microsoft/ProcMon-for-Linux/releases '''
        def download(self, target_dir="sysinternals/procmon", tagVer="latest"):
            if "linux" == platform.system().lower():
                downUrl = GITHUB_RELEASES(source="Sysinternals/ProcMon-for-Linux").geturl("procmon.*?\.tar\.gz", tagVer)
                resp = HTTPGET(downUrl)
                raise NotImplementedError("linux procmon not implemented")
            else:
                downUrl = "https://download.sysinternals.com/files/ProcessMonitor.zip"
                resp = HTTPGET(downUrl)
                if (200 == resp.status):
                    return EXTRACT.zip(resp.read(), target_dir=target_dir)

            raise Exception("download failed: " + downUrl)

    class ProcDump:
        ''' https://github.com/microsoft/ProcDump-for-Linux/releases '''
        ''' https://github.com/microsoft/ProcDump-for-Mac/releases '''
        def download(self, target_dir="sysinternals/procdump", tagVer="latest"):
            if "linux" == platform.system().lower():
                downUrl = GITHUB_RELEASES(source="microsoft/ProcDump-for-Linux").geturl("procdump.*?\.tar\.gz", tagVer)
                resp = HTTPGET(downUrl)
                raise NotImplementedError("linux procdump not implemented")
            elif "darwin" == platform.system().lower():
                downUrl = GITHUB_RELEASES(source="microsoft/ProcDump-for-Mac").geturl("procdump.*?\.tar\.gz", tagVer)
                resp = HTTPGET(downUrl)
                raise NotImplementedError("osx procdump not implemented")
            else:
                downUrl = "https://download.sysinternals.com/files/Procdump.zip"
                resp = HTTPGET(downUrl)
                if (200 == resp.status):
                    return EXTRACT.zip(resp.read(), target_dir=target_dir)

            raise Exception("download failed: " + downUrl)


class dbbrowser:

    class sqlitebrowser:
        ''' https://github.com/sqlitebrowser/sqlitebrowser/releases '''
        def download(self, target_dir="sqlitebrowser", tagVer="latest"):
            if (os.path.exists(target_dir)): return target_dir

            downUrl = GITHUB_RELEASES(source="sqlitebrowser/sqlitebrowser").geturl("DB.Browser.for.SQLite.*?\.zip", tagVer)
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir=target_dir)

            raise Exception("download failed: " + downUrl)

    class dbeaver:
        ''' https://github.com/dbeaver/dbeaver/releases '''
        def download(self, target_dir="dbeaver", tagVer="latest"):
            if (os.path.exists(target_dir)): return target_dir

            downUrl = GITHUB_RELEASES(source="dbeaver/dbeaver").geturl("dbeaver-ce-.*?\.zip", tagVer)
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir='.')

            raise Exception("download failed: " + downUrl)


class misc:

    class DIEengine:
        ''' https://github.com/horsicq/DIE-engine/releases '''
        def download(self, target_dir="die-engine", tagVer="latest"):
            downUrl = GITHUB_RELEASES(source="horsicq/DIE-engine").geturl("die_win64_portable_.*?\.zip", tagVer)
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir=target_dir)

            raise Exception("download failed: " + downUrl)

    class UPX:
        ''' https://github.com/upx/upx/releases '''
        def download(self, target_dir="upx", tagVer="latest"):
            downUrl = GITHUB_RELEASES(source="upx/upx").geturl("upx-.*?win64\.zip", tagVer)
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir='.')

            raise Exception("download failed: " + downUrl)

    class WinObjEx64:
        ''' https://github.com/hfiref0x/WinObjEx64/releases '''
        def download(self, target_dir="WinObjEx64", tagVer="latest"):
            downUrl = GITHUB_RELEASES(source="hfiref0x/WinObjEx64").geturl("winobjex64.*?\.zip", tagVer)
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir=target_dir)

            raise Exception("download failed: " + downUrl)

    class WinMerge:
        ''' https://github.com/WinMerge/winmerge/releases '''
        def download(self, target_dir="WinMerge", tagVer="latest"):
            if (os.path.exists(target_dir)): return target_dir

            def zipfilter(m:zipfile.ZipInfo):
                if (re.match(r"^WinMerge/", m.filename)):
                    m.filename = re.sub(r"^WinMerge/", "/", m.filename)
                    return True
                return False

            downUrl = GITHUB_RELEASES(source="WinMerge/winmerge").geturl("winmerge-.*?-x64-exe\.zip", tagVer)
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir=target_dir, zipfilter=zipfilter)

            raise Exception("download failed: " + downUrl)

    class Hexer:
        ''' https://github.com/jovibor/Hexer/releases '''
        def download(self, target_dir="Hexer", tagVer="latest"):
            downUrl = GITHUB_RELEASES(source="jovibor/Hexer").geturl("Hexer_.*?\.rar", tagVer)
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                raise NotImplementedError("rar file not support yet")

            raise Exception("download failed: " + downUrl)

    class NamedPipeMaster:
        ''' https://github.com/zeze-zeze/NamedPipeMaster/releases '''
        def download(self, target_dir="NamedPipeMaster", tagVer="latest"):
            downUrl = GITHUB_RELEASES(source="zeze-zeze/NamedPipeMaster").geturl("NamedPipeMaster-64bit\.zip", tagVer)
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir=target_dir)

            raise Exception("download failed: " + downUrl)

    class dnGrep:
        ''' https://github.com/dnGrep/dnGrep/releases '''
        def download(self, target_dir="dnGrep", tagVer="latest"):
            downUrl = GITHUB_RELEASES(source="dnGrep/dnGrep").geturl("dnGrep.*?x64\.zip", tagVer)
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir=target_dir)

            raise Exception("download failed: " + downUrl)

    class wmie2:
        ''' https://github.com/chrislogan2/wmie2/releases '''
        def download(self, target_dir="wmie2", tagVer="v2.0.1.x"):
            downUrl = GITHUB_RELEASES(source="chrislogan2/wmie2").geturl("WmiExplorer.*?\.zip", tagVer)
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir=target_dir)

            raise Exception("download failed: " + downUrl)

    class fasm2:
        ''' https://github.com/tgrysztar/fasm2 '''
        def download(self, target_dir="fasm2", tagVer="latest"):
            def zipfilter(m:zipfile.ZipInfo):
                if (re.match(r"^fasm2-master/", m.filename)):
                    m.filename = re.sub(r"^fasm2-master/", "/", m.filename)
                    return True
                return False

            downUrl = "https://github.com/tgrysztar/fasm2" \
                "/archive/" "master" ".zip"
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir=target_dir, zipfilter=zipfilter)

            raise Exception("download failed: " + downUrl)

    class resourcehacker:
        def download(self, target_dir="resourcehacker"):
            if (os.path.exists(target_dir)): return target_dir

            downUrl = "http://angusj.com/resourcehacker/resource_hacker.zip"
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir=target_dir)

    class exiftool:
        def download(self, target_dir="exiftool"):
            downUrl = "https://sourceforge.net/projects/exiftool/files/latest/download"
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir=target_dir)

    class trid:
        def download(self, target_dir="trid"):
            downUrl = "http://mark0.net/download/triddefs.zip"
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir=target_dir) \
                    and EXTRACT.zip(HTTPGET("http://mark0.net/download/trid_w32.zip").read(), target_dir=target_dir)

    class WinHex:
        def download(self, target_dir="WinHex"):
            downUrl = "https://github.com/GTHF/trash_package/raw/main/" \
                "WinHex_v19.6_SR2.zip"

            def license(target_dir):
                ''' do you have a license? '''
                target = os.path.join(target_dir, "user.txt")
                return target

            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir=target_dir) \
                    # and license(target_dir=target_dir)

    class KmdManager:
        def download(self, target_dir="KmdManager"):
            downUrl = "https://github.com/GTHF/trash_package/raw/main/KmdManager.exe"
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.bin(resp.read(), target_dir='.', target_name=os.path.basename(downUrl)) \

    class guidedhacking:
        '''  '''

        class GHInjector:
            ''' https://github.com/guidedhacking/GuidedHacking-Injector/releases '''
            def download(self, target_dir="GH/Injector"):
                ''' https://guidedhacking.com/resources/guided-hacking-dll-injector.4/download '''
                downUrl = "https://github.com/GTHF/trash_package/raw/main/GH/GH%20Injector.zip"
                resp = HTTPGET(downUrl)
                if (200 == resp.status):
                    return EXTRACT.zip(resp.read(), target_dir=target_dir)

        class GHCheatEngine:
            ''' https://github.com/cheat-engine/cheat-engine/releases '''
            def download(self, target_dir="GH/AesopEngine"):
                ''' https://guidedhacking.com/resources/gh-undetected-cheat-engine-download-udce-driver.14/download '''
                downUrl = "https://github.com/GTHF/trash_package/raw/main/GH/AesopEngine.zip"
                resp = HTTPGET(downUrl)
                if (200 == resp.status):
                    UEDumperUrl = "https://github.com/GTHF/trash_package/raw/main/GH/GH_UE_Dumper.zip"
                    return EXTRACT.zip(HTTPGET(UEDumperUrl).read(), target_dir=target_dir) and \
                        EXTRACT.zip(resp.read(), target_dir=os.path.dirname(target_dir))


class WinArk:
    ''' Windows Anti-Rootkit '''

    class SystemInformer:
        ''' https://github.com/winsiderss/systeminformer '''
        def download(self, target_dir="systeminformer", tagVer="latest"):
            downUrl = GITHUB_RELEASES(source="winsiderss/si-builds").geturl("systeminformer-.*?-release-bin\.zip", tagVer)
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir=target_dir)

            raise Exception("download failed: " + downUrl)

    class WinArk:
        ''' https://github.com/BeneficialCode/WinArk/releases '''

    class winsecark:
        ''' https://github.com/i1tao/winsec-ark/releases '''

    class WKE:
        def download(self, target_dir="winark"):
            downUrl = "https://github.com/AxtMueller/Windows-Kernel-Explorer" \
                "/archive/" "master" ".zip"
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir=target_dir)

    class Pyark:
        def download(self, target_dir="winark/Pyark"):
            downUrl = "https://github.com/antiwar3/py" \
                "/blob/" "master" "/Pyark.zip?raw=true"
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir=target_dir)

    class WKTools:
        def download(self, target_dir="winark/WKTools"):
            downUrl = "https://github.com/AngleHony/WKTools" \
                "/blob/" "main" "/WKTools.exe?raw=true"
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.bin(resp.read(), target_dir=target_dir, target_name="WKTools.exe")

    class YDArk:
        ''' driver file not signed '''
        def download(self, target_dir="winark/YDArk"):
            downUrl = "https://github.com/ClownQq/YDArk" \
                "/archive/" "master" ".zip"
            downUrl = "https://github.com/GTHF/trash_package/raw/main/" \
                "YDArk-1.0.3.3-signed.zip"
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir=target_dir)



if __name__ == "__main__":

    x64DBG = debugger.x64dbg().download(); \
        misc.DIEengine().download(); \
        misc.UPX().download(); \
        misc.WinHex().download(); \
        misc.WinMerge().download(); \
        misc.guidedhacking.GHInjector().download(); \
        misc.guidedhacking.GHCheatEngine().download(); \
        misc.fasm2().download(); \

    dbbrowser.sqlitebrowser().download(); \

    dumper.ksdumper().download(); \
        dumper.winchecksec().download(); \
        dumper.hollowshunter().download(); \
        # dumper.binskim().download(); \

    WinArk.SystemInformer().download(); \
        WinArk.WKE().download(); \
        WinArk.Pyark().download(); \
        # WinArk.WKTools().download(); \
        # WinArk.YDArk().download(); \

    sysinternals.ProcessExplorer().download(); \
        sysinternals.ProcessMonitor().download(); \
        sysinternals.PSTools().download(); \
        sysinternals.ProcDump().download(); \
        sysinternals.Sysmon().download(); \
        sysinternals.WinObj().download(); \
        sysinternals.Testlimit().download(); \
        sysinternals.DebugView().download(); \

    # if (input("plug-in download? (y/n):").lower().startswith("y")):
    #     debugger.x64dbg.plugin(x64DBG)
