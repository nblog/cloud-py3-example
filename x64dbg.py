#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, io, sys, re, types, platform, subprocess, urllib.request, zipfile

HTTPGET = urllib.request.urlopen

if not "DEBUGPY_RUNNING" in os.environ:
    source = "utils/common"
    RAW_CODE = HTTPGET(f"https://github.com/nblog/cloud-py3-example/blob/main/{source}.py?raw=true").read().decode('utf-8')

    raw_module = types.ModuleType(source.split('/')[-1])
    sys.modules[source.replace('/', '.')] = raw_module
    exec(RAW_CODE, raw_module.__dict__)

from utils.common import (
    EXTRACT, GITHUB_RELEASES, download2
)


class dumper:

    class binskim:
        ''' https://github.com/microsoft/binskim/releases '''
        def download(self, target_dir="binskim", tagVer="latest"):
            if (os.path.exists(target_dir)): return target_dir

            def zipfilter(f:zipfile.ZipInfo):
                f.filename = re.sub(r"^tools/net9.0/win-x64/", "/", f.filename)
                return True

            m = re.search(r'(\d+\.\d+\.\d+)', tagVer)
            downUrl = "/".join([
                "https://www.nuget.org/api/v2/package",
                "Microsoft.CodeAnalysis.BinSkim", 
                m.group(0) if m else ('' if "latest" == tagVer else tagVer),
            ])
            return EXTRACT.zip(download2(downUrl), target_dir=target_dir, zipfilter=zipfilter)

    class blint:
        ''' https://github.com/owasp-dep-scan/blint/releases '''
        def download(self, target_dir="blint", tagVer="latest"):
            downUrl = GITHUB_RELEASES(source="owasp-dep-scan/blint").geturl("blint.exe", tagVer)
            return EXTRACT.bin(download2(downUrl), target_dir=target_dir, target_name="blint.exe")

    class winchecksec:
        ''' https://github.com/trailofbits/winchecksec/releases '''
        def download(self, target_dir="winchecksec", tagVer="latest"):
            def zipfilter(f:zipfile.ZipInfo):
                f.filename = re.sub(r"^build/Release/", "/", f.filename)
                return True

            downUrl = GITHUB_RELEASES(source="trailofbits/winchecksec").geturl("windows.x64.Release.zip", tagVer)
            return EXTRACT.zip(download2(downUrl), target_dir=target_dir, zipfilter=zipfilter)

    class ksdumper:
        ''' https://github.com/mastercodeon31415/KsDumper-11/releases '''
        def download(self, target_dir="ksdumper", tagVer="latest"):
            downUrl = GITHUB_RELEASES(source="mastercodeon31415/KsDumper-11").geturl("KsDumper.*?.zip", tagVer)
            return EXTRACT.zip(download2(downUrl), target_dir=target_dir)

    class hollowshunter:
        ''' https://github.com/hasherezade/hollows_hunter '''
        def download(self, target_dir="hollowshunter", tagVer="latest"):
            downUrl = GITHUB_RELEASES(source="hasherezade/hollows_hunter").geturl("hollows_hunter64.zip", tagVer)
            return EXTRACT.zip(download2(downUrl), target_dir=target_dir)

    class oleviewdotnet:
        ''' https://github.com/tyranid/oleviewdotnet/releases '''

    class ReClassNET:
        ''' https://github.com/ReClassNET/ReClass.NET/releases '''


class debugger:

    class x64dbg:
        ''' https://github.com/x64dbg/x64dbg/releases '''
        def download(self, target_dir="x64dbg", tagVer="latest"):
            downUrl = GITHUB_RELEASES(source="x64dbg/x64dbg").geturl("snapshot_.*?.zip", tagVer)
            return EXTRACT.zip(download2(downUrl), target_dir=target_dir)

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
                def zipfilter(f:zipfile.ZipInfo):
                    f.filename = re.sub(r"^SharpOD_x64_v0.6d Stable/x64dbg/", "/", f.filename)
                    return True

                downUrl = "https://down.52pojie.cn/Tools/OllyDbg_Plugin/SharpOD_x64_v0.6d_Stable.zip"
                return EXTRACT.zip(download2(downUrl), target_dir=os.path.join(target_dir, "release"), zipfilter=zipfilter)

            return \
                ScyllaHide(target_dir) \
                    or TitanHide(target_dir) \
                    or SharpOD(target_dir)

    class cutter:
        ''' https://github.com/rizinorg/cutter/releases '''
        def download(self, target_dir="cutter", tagVer="latest"):
            downUrl = GITHUB_RELEASES(source="rizinorg/cutter").geturl("Cutter.*?.zip", tagVer)
            return EXTRACT.zip(download2(downUrl), target_dir='.')


class sysinternals:
    ''' https://download.sysinternals.com/files/SysinternalsSuite.zip '''
    ''' https://download.sysinternals.com/files/SysinternalsSuite-ARM64.zip '''

    class ZoomIt:
        def download(self, target_dir="sysinternals/zoomit"):
            downUrl = "https://download.sysinternals.com/files/ZoomIt.zip"
            return EXTRACT.zip(download2(downUrl), target_dir=target_dir)

    class BGInfo:
        def download(self, target_dir="sysinternals/bginfo"):
            downUrl = "https://download.sysinternals.com/files/BGInfo.zip"
            return EXTRACT.zip(download2(downUrl), target_dir=target_dir)

    class Testlimit:
        def download(self, target_dir="sysinternals/testlimit"):
            downUrl = "https://download.sysinternals.com/files/Testlimit.zip"
            return EXTRACT.zip(download2(downUrl), target_dir=target_dir)

    class DebugView:
        def download(self, target_dir="sysinternals/debugview"):
            downUrl = "https://download.sysinternals.com/files/DebugView.zip"
            return EXTRACT.zip(download2(downUrl), target_dir=target_dir)

    class ProcessExplorer:
        def download(self, target_dir="sysinternals/procexp"):
            downUrl = "https://download.sysinternals.com/files/ProcessExplorer.zip"
            return EXTRACT.zip(download2(downUrl), target_dir=target_dir)

    class PSTools:
        def download(self, target_dir="sysinternals/pstools"):
            downUrl = "https://download.sysinternals.com/files/PSTools.zip"
            return EXTRACT.zip(download2(downUrl), target_dir=target_dir)

    class WinObj:
        def download(self, target_dir="sysinternals/winobj"):
            downUrl = "https://download.sysinternals.com/files/WinObj.zip"
            return EXTRACT.zip(download2(downUrl), target_dir=target_dir)

    class Coreinfo:
        def download(self, target_dir="sysinternals/coreinfo"):
            downUrl = "https://download.sysinternals.com/files/Coreinfo.zip"
            return EXTRACT.zip(download2(downUrl), target_dir=target_dir)

    class Sysmon:
        ''' https://github.com/microsoft/SysinternalsEBPF/releases '''
        ''' https://github.com/microsoft/SysmonForLinux/releases '''
        def download(self, target_dir="sysinternals/sysmon", tagVer="latest"):
            if "linux" == platform.system().lower():
                downUrl = GITHUB_RELEASES(source="Sysinternals/SysmonForLinux").geturl("sysmonforlinux.*?.tar.gz", tagVer)
                download2(downUrl)  # linux sysmon not implemented
                raise NotImplementedError("linux sysmon not implemented")
            else:
                downUrl = "https://download.sysinternals.com/files/Sysmon.zip"
                return EXTRACT.zip(download2(downUrl), target_dir=target_dir)

    class ProcessMonitor:
        ''' https://github.com/microsoft/ProcMon-for-Linux/releases '''
        def download(self, target_dir="sysinternals/procmon", tagVer="latest"):
            if "linux" == platform.system().lower():
                downUrl = GITHUB_RELEASES(source="Sysinternals/ProcMon-for-Linux").geturl("procmon.*?.tar.gz", tagVer)
                download2(downUrl)  # linux procmon not implemented
                raise NotImplementedError("linux procmon not implemented")
            else:
                downUrl = "https://download.sysinternals.com/files/ProcessMonitor.zip"
                return EXTRACT.zip(download2(downUrl), target_dir=target_dir)

    class ProcDump:
        ''' https://github.com/microsoft/elfcore '''
        ''' https://github.com/microsoft/ProcDump-for-Linux/releases '''
        ''' https://github.com/microsoft/ProcDump-for-Mac/releases '''
        def download(self, target_dir="sysinternals/procdump", tagVer="latest"):
            if "linux" == platform.system().lower():
                downUrl = GITHUB_RELEASES(source="microsoft/ProcDump-for-Linux").geturl("procdump.*?.tar.gz", tagVer)
                download2(downUrl)  # linux procdump not implemented
                raise NotImplementedError("linux procdump not implemented")
            elif "darwin" == platform.system().lower():
                downUrl = GITHUB_RELEASES(source="microsoft/ProcDump-for-Mac").geturl("procdump.*?.tar.gz", tagVer)
                download2(downUrl)  # osx procdump not implemented
                raise NotImplementedError("osx procdump not implemented")
            else:
                downUrl = "https://download.sysinternals.com/files/Procdump.zip"
                return EXTRACT.zip(download2(downUrl), target_dir=target_dir)


class dbbrowser:

    class sqlitebrowser:
        ''' https://github.com/sqlitebrowser/sqlitebrowser/releases '''
        def download(self, target_dir="sqlitebrowser", tagVer="latest"):
            if (os.path.exists(target_dir)): return target_dir

            downUrl = GITHUB_RELEASES(source="sqlitebrowser/sqlitebrowser").geturl("DB.Browser.for.SQLite.*?.zip", tagVer)
            return EXTRACT.zip(download2(downUrl), target_dir=target_dir)

    class dbeaver:
        ''' https://github.com/dbeaver/dbeaver/releases '''
        def download(self, target_dir="dbeaver", tagVer="latest"):
            if (os.path.exists(target_dir)): return target_dir

            downUrl = GITHUB_RELEASES(source="dbeaver/dbeaver").geturl("dbeaver-ce-.*?.zip", tagVer)
            return EXTRACT.zip(download2(downUrl), target_dir='.')


class misc:

    class DIEengine:
        ''' https://github.com/horsicq/DIE-engine/releases '''
        def download(self, target_dir="die-engine", tagVer="latest"):
            downUrl = GITHUB_RELEASES(source="horsicq/DIE-engine").geturl("die_win64_portable_.*?.zip", tagVer)
            return EXTRACT.zip(download2(downUrl), target_dir=target_dir)

    class UPX:
        ''' https://github.com/upx/upx/releases '''
        def download(self, target_dir="upx", tagVer="latest"):
            downUrl = GITHUB_RELEASES(source="upx/upx").geturl("upx-.*?win64.zip", tagVer)
            return EXTRACT.zip(download2(downUrl), target_dir='.')

    class WinObjEx64:
        ''' https://github.com/hfiref0x/WinObjEx64/releases '''
        def download(self, target_dir="WinObjEx64", tagVer="latest"):
            downUrl = GITHUB_RELEASES(source="hfiref0x/WinObjEx64").geturl("winobjex64.*?.zip", tagVer)
            return EXTRACT.zip(download2(downUrl), target_dir=target_dir)

    class WinMerge:
        ''' https://github.com/WinMerge/winmerge/releases '''
        def download(self, target_dir="WinMerge", tagVer="latest"):
            if (os.path.exists(target_dir)): return target_dir

            def zipfilter(f:zipfile.ZipInfo):
                f.filename = re.sub(r"^WinMerge/", "/", f.filename)
                return True

            downUrl = GITHUB_RELEASES(source="WinMerge/winmerge").geturl("winmerge-.*?-x64-exe.zip", tagVer)
            return EXTRACT.zip(download2(downUrl), target_dir=target_dir, zipfilter=zipfilter)

    class Hexer:
        ''' https://github.com/jovibor/Hexer/releases '''
        def download(self, target_dir="Hexer", tagVer="latest"):
            downUrl = GITHUB_RELEASES(source="jovibor/Hexer").geturl("Hexer_.*?.rar", tagVer)
            download2(downUrl)  # rar file not support yet
            raise NotImplementedError("rar file not support yet")

    class NamedPipeMaster:
        ''' https://github.com/zeze-zeze/NamedPipeMaster/releases '''
        def download(self, target_dir="NamedPipeMaster", tagVer="latest"):
            downUrl = GITHUB_RELEASES(source="zeze-zeze/NamedPipeMaster").geturl("NamedPipeMaster-64bit.zip", tagVer)
            return EXTRACT.zip(download2(downUrl), target_dir=target_dir)

    class dnGrep:
        ''' https://github.com/dnGrep/dnGrep/releases '''
        def download(self, target_dir="dnGrep", tagVer="latest"):
            downUrl = GITHUB_RELEASES(source="dnGrep/dnGrep").geturl("dnGrep.*?x64.zip", tagVer)
            return EXTRACT.zip(download2(downUrl), target_dir=target_dir)

    class wmie2:
        ''' https://github.com/chrislogan2/wmie2/releases '''
        def download(self, target_dir="wmie2", tagVer="v2.0.1.x"):
            downUrl = GITHUB_RELEASES(source="chrislogan2/wmie2").geturl("WmiExplorer.*?.zip", tagVer)
            return EXTRACT.zip(download2(downUrl), target_dir=target_dir)

    class fasm2:
        ''' https://github.com/tgrysztar/fasm2 '''
        def download(self, target_dir="fasm2", tagVer="latest"):
            def zipfilter(f:zipfile.ZipInfo):
                f.filename = re.sub(r"^fasm2-master/", "/", f.filename)
                return True

            downUrl = "https://github.com/tgrysztar/fasm2" \
                "/archive/" "master" ".zip"
            return EXTRACT.zip(download2(downUrl), target_dir=target_dir, zipfilter=zipfilter)

    class resourcehacker:
        def download(self, target_dir="resourcehacker"):
            if (os.path.exists(target_dir)): return target_dir

            downUrl = "http://angusj.com/resourcehacker/resource_hacker.zip"
            return EXTRACT.zip(download2(downUrl), target_dir=target_dir)

    class exiftool:
        def download(self, target_dir="exiftool"):
            downUrl = "https://sourceforge.net/projects/exiftool/files/latest/download"
            return EXTRACT.zip(download2(downUrl), target_dir=target_dir)

    class trid:
        def download(self, target_dir="trid"):
            return EXTRACT.zip(download2("https://mark0.net/download/triddefs.zip"), target_dir=target_dir) \
                and EXTRACT.zip(download2("https://mark0.net/download/trid_win64.zip"), target_dir=target_dir)

    class WinHex:
        def download(self, target_dir="WinHex"):
            downUrl = "https://github.com/GTHF/trash_package/raw/main/" \
                "WinHex_v19.6_SR2.zip"

            import datetime
            if datetime.datetime.now() > datetime.datetime(2026, 11, 22):
                return EXTRACT.zip(download2(downUrl), target_dir=target_dir)

            def license(target_dir):
                ''' do you have a license? '''
                license_txt = '''
// WinHex license file

Name: semthex
Addr: ru-board.com
Addr: RUSSIA
Data: 21C99167CC69236A2EB9540CF881EFF6
Data: 2376D8CC4E33860CF5A9E379945DA0BE
Cksm: 3DD34CCA
'''
                with open(os.path.join(target_dir, "user.txt"), "w") as f:
                    f.write(license_txt.strip())
                return target_dir

            EXTRACT.zip(download2("https://www.x-ways.net/winhex.zip"), target_dir=target_dir)
            return EXTRACT.zip(download2("https://www.x-ways.net/winhex-x64-addon.zip"), target_dir=target_dir) \
                and license(target_dir=target_dir)

    class KmdManager:
        def download(self, target_dir="KmdManager"):
            downUrl = "https://github.com/GTHF/trash_package/raw/main/KmdManager.exe"
            return EXTRACT.bin(download2(downUrl), target_dir='.', target_name=os.path.basename(downUrl))

    class guidedhacking:
        '''  '''

        class GHInjector:
            ''' https://github.com/guidedhacking/GuidedHacking-Injector/releases '''
            def download(self, target_dir="GH/Injector"):
                ''' https://guidedhacking.com/resources/guided-hacking-dll-injector.4/download '''
                downUrl = "https://github.com/GTHF/trash_package/raw/main/GH/GH_Injector.zip"
                return EXTRACT.zip(download2(downUrl), target_dir=target_dir)

        class GHCheatEngine:
            ''' https://github.com/cheat-engine/cheat-engine/releases '''
            def download(self, target_dir="GH/AesopEngine"):
                ''' https://guidedhacking.com/resources/gh-undetected-cheat-engine-download-udce-driver.14/download '''
                downUrl = "https://github.com/GTHF/trash_package/raw/main/GH/AesopEngine.zip"
                UEDumperUrl = "https://github.com/GTHF/trash_package/raw/main/GH/GH_UE_Dumper.zip"
                return EXTRACT.zip(download2(UEDumperUrl), target_dir=target_dir) and \
                    EXTRACT.zip(download2(downUrl), target_dir=os.path.dirname(target_dir))


class WinArk:
    ''' Windows Anti-Rootkit '''

    class SystemInformer:
        ''' https://github.com/winsiderss/systeminformer '''
        def download(self, target_dir="systeminformer", tagVer="latest"):
            downUrl = GITHUB_RELEASES(source="winsiderss/si-builds").geturl("systeminformer-build-bin.zip", tagVer)
            return EXTRACT.zip(download2(downUrl), target_dir=target_dir)

    class WinArk:
        ''' https://github.com/BeneficialCode/WinArk/releases '''

    class winsecark:
        ''' https://github.com/i1tao/winsec-ark/releases '''

    class QDoctor:
        def download(self, target_dir="WinArk"):
            downUrl = GITHUB_RELEASES(source="QAX-Anti-Virus/QDoctor").geturl("QDoctor.*?.exe", tagVer="latest")
            return EXTRACT.bin(download2(downUrl), target_dir=target_dir, target_name="QDoctor.exe")

    class WKE:
        def download(self, target_dir="WinArk"):
            downUrl = "https://github.com/AxtMueller/Windows-Kernel-Explorer" \
                "/archive/" "master" ".zip"
            return EXTRACT.zip(download2(downUrl), target_dir=target_dir)

    class Pyark:
        def download(self, target_dir="WinArk/Pyark"):
            downUrl = "https://github.com/antiwar3/py" \
                "/blob/" "master" "/Pyark.zip?raw=true"
            downUrl = GITHUB_RELEASES(source="antiwar3/py").geturl("Pyark.zip", tagVer="latest")
            return EXTRACT.zip(download2(downUrl), target_dir=target_dir)

    class WKTools:
        def download(self, target_dir="WinArk/WKTools"):
            downUrl = "https://github.com/AngleHony/WKTools" \
                "/blob/" "main" "/WKTools.exe?raw=true"
            return EXTRACT.bin(download2(downUrl), target_dir=target_dir, target_name="WKTools.exe")

    class SKT64:
        def download(self, target_dir="WinArk/SKT64"):
            downUrl = "https://github.com/PspExitThread/SKT64" \
                "blob/" "main" "/SKT64-Release.exe?raw=true"
            return EXTRACT.bin(download2(downUrl), target_dir=target_dir, target_name="SKT64.exe")

    class NoOne:
        def download(self, target_dir="WinArk/NoOne"):
            downUrl = "https://github.com/k273811702/NoOne"

    class YDArk:
        ''' driver file not signed '''
        def download(self, target_dir="WinArk/YDArk"):
            downUrl = "https://github.com/ClownQq/YDArk" \
                "/archive/" "master" ".zip"
            downUrl = "https://github.com/GTHF/trash_package/raw/main/" \
                "YDArk-1.0.3.3-signed.zip"
            return EXTRACT.zip(download2(downUrl), target_dir=target_dir)



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
        dbbrowser.dbeaver().download(); \

    dumper.binskim().download(); \
        dumper.hollowshunter().download(); \
        dumper.ksdumper().download(); \
        # dumper.blint().download(); \
        # dumper.winchecksec().download(); \

    WinArk.SystemInformer().download(); \
        WinArk.QDoctor().download(); \
        WinArk.WKE().download(); \
        WinArk.Pyark().download(); \
        WinArk.WKTools().download(); \
        # WinArk.SKT64().download(); \

    sysinternals.ProcessExplorer().download(); \
        sysinternals.ProcessMonitor().download(); \
        sysinternals.Sysmon().download(); \
        sysinternals.ProcDump().download(); \
        sysinternals.DebugView().download(); \
        sysinternals.WinObj().download(); \
        sysinternals.Coreinfo().download(); \
        sysinternals.PSTools().download(); \
        sysinternals.Testlimit().download(); \
        sysinternals.BGInfo().download(); \
        sysinternals.ZoomIt().download(); \

    # if (input("plug-in download? (y/[n]):").lower().startswith("y")):
    #     debugger.x64dbg.plugin(x64DBG)
