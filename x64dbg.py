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



class dumper:

    class ksdumper:

        RELEASES_URL = "https://github.com/mastercodeon314/KsDumper-11/releases"

        def latest(self):
            resp = HTTPGET( "/".join([self.RELEASES_URL, "latest"]) )
            tagVer = str(resp.url).split("tag/")[-1]
            return tagVer

        def assets(self, tagVer):
            resp = HTTPGET( "/".join([self.RELEASES_URL, "expanded_assets", tagVer]) )
            assets = re.findall(">(KsDumper11.*?.zip)<", resp.read().decode())
            return assets

        def download(self, tagVer="latest", target_dir='ksdumper'):
            if tagVer == "latest": tagVer = self.latest()
            target = self.assets(tagVer)[0]
            downUrl = "/".join([self.RELEASES_URL, "download", tagVer, target])
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir=target_dir)

            raise Exception("download failed: " + downUrl)

    class binskim:

        RELEASES_URL = "https://github.com/microsoft/binskim/releases"

        def latest(self):
            resp = HTTPGET( "/".join([self.RELEASES_URL, "latest"]) )
            tagVer = str(resp.url).split("tag/")[-1]
            return tagVer

        def download(self, tagVer="latest", target_dir='binskim'):
            if tagVer == "latest": tagVer = self.latest()

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

        RELEASES_URL = "https://github.com/trailofbits/winchecksec/releases"

        def latest(self):
            resp = HTTPGET( "/".join([self.RELEASES_URL, "latest"]) )
            tagVer = str(resp.url).split("tag/")[-1]
            return tagVer

        def assets(self, tagVer):
            resp = HTTPGET( "/".join([self.RELEASES_URL, "expanded_assets", tagVer]) )
            assets = re.findall(">(windows.x64.Release.zip)<", resp.read().decode())
            return assets

        def download(self, tagVer="latest", target_dir='winchecksec'):
            if tagVer == "latest": tagVer = self.latest()
            target = self.assets(tagVer)[0]

            def zipfilter(m:zipfile.ZipInfo):
                if (re.match(r"^build/Release", m.filename)):
                    m.filename = re.sub(r"^build/Release", "", m.filename)
                    return True
                return False

            downUrl = "/".join([self.RELEASES_URL, "download", tagVer, target])
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir=target_dir, zipfilter=zipfilter)

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

    class pe_sieve:

        RELEASES_URL = "https://github.com/hasherezade/pe-sieve/releases"

        def latest(self):
            resp = HTTPGET( "/".join([self.RELEASES_URL, "latest"]) )
            tagVer = str(resp.url).split("tag/")[-1]
            return tagVer

        def assets(self, tagVer):
            resp = HTTPGET( "/".join([self.RELEASES_URL, "expanded_assets", tagVer]) )
            assets = re.findall(">(pe-sieve64.zip)<", resp.read().decode())
            return assets

        def download(self, tagVer="latest", target_dir='pe-sieve'):
            if tagVer == "latest": tagVer = self.latest()
            target = self.assets(tagVer)[0]
            downUrl = "/".join([self.RELEASES_URL, "download", tagVer, target])
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir=target_dir)

            raise Exception("download failed: " + downUrl)

    class oleviewdotnet:

        RELEASES_URL = "https://github.com/tyranid/oleviewdotnet/releases"

    class pe_unmapper:

        RELEASES_URL = "https://github.com/hasherezade/pe_unmapper/releases"

    class process_dump:

        RELEASES_URL = "https://github.com/glmcdona/Process-Dump/releases"



class debugger:

    class x64dbg:

        RELEASES_URL = "https://github.com/x64dbg/x64dbg/releases"

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
                return EXTRACT.zip(resp.read(), target_dir=target_dir)

            raise Exception("download failed: " + downUrl)

        @staticmethod
        def plugin(target_dir):
            ''' x64dbg plugin '''
            def ScyllaHide(target_dir):
                ''' https://github.com/x64dbg/ScyllaHide/releases '''

            def TitanHide(target_dir):
                ''' https://github.com/mrexodia/TitanHide/releases '''

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

            def OllyDumpEx(target_dir):
                ''' https://low-priority.appspot.com/ollydumpex/OllyDumpEx.zip '''

            def Multiline_Ultimate_Assembler(target_dir):
                ''' https://ramensoftware.com/downloads/multiasm.rar '''

            return \
                ScyllaHide(target_dir) \
                    or TitanHide(target_dir) \
                    or SharpOD(target_dir)

    class cutter:

        RELEASES_URL = "https://github.com/rizinorg/cutter/releases"

        def latest(self):
            resp = HTTPGET( "/".join([self.RELEASES_URL, "latest"]) )
            tagVer = str(resp.url).split("tag/")[-1]
            return tagVer

        def assets(self, tagVer):
            resp = HTTPGET( "/".join([self.RELEASES_URL, "expanded_assets", tagVer]) )
            assets = re.findall(">(Cutter.*?.zip)<", resp.read().decode())
            return assets

        def download(self, tagVer="latest", target_dir='cutter'):
            if tagVer == "latest": tagVer = self.latest()
            target = self.assets(tagVer)[0]
            downUrl = "/".join([self.RELEASES_URL, "download", tagVer, target])
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir='.')

            raise Exception("download failed: " + downUrl)



class sysinternals:
    ''' https://download.sysinternals.com/files/SysinternalsSuite.zip '''
    ''' https://download.sysinternals.com/files/SysinternalsSuite-ARM64.zip '''


    class debugview:
        def download(self, target_dir='debugview'):
            downUrl = "https://download.sysinternals.com/files/DebugView.zip"
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir=os.path.join("sysinternals", target_dir))

    class procexp:
        def download(self, target_dir='procexp'):
            downUrl = "https://download.sysinternals.com/files/ProcessExplorer.zip"
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir=os.path.join("sysinternals", target_dir))

    class pstools:
        def download(self, target_dir='pstools'):
            downUrl = "https://download.sysinternals.com/files/PSTools.zip"
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir=os.path.join("sysinternals", target_dir))

    class winobj:
        def download(self, target_dir='winobj'):
            downUrl = "https://download.sysinternals.com/files/WinObj.zip"
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir=os.path.join("sysinternals", target_dir))

    class sysmon:

        RELEASES_URL = "https://github.com/Sysinternals/SysmonForLinux/releases/"

        def latest(self):
            resp = HTTPGET( "/".join([self.RELEASES_URL, "latest"]) )
            tagVer = str(resp.url).split("tag/")[-1]
            return tagVer

        def assets(self, tagVer):
            resp = HTTPGET( "/".join([self.RELEASES_URL, "expanded_assets", tagVer]) )
            assets = re.findall(">(sysmonforlinux.*?.tar.gz)<", resp.read().decode())
            return assets

        def download(self, tagVer="latest", target_dir='sysmon'):
            if "linux" == platform.system().lower():
                if tagVer == "latest": tagVer = self.latest()
                target = self.assets(tagVer)[0]
                downUrl = "/".join([self.RELEASES_URL, "download", tagVer, target])
                resp = HTTPGET(downUrl)
                raise NotImplementedError("linux sysmon not implemented")
            else:
                downUrl = "https://download.sysinternals.com/files/Sysmon.zip"
                resp = HTTPGET(downUrl)
                if (200 == resp.status):
                    return EXTRACT.zip(resp.read(), target_dir=os.path.join("sysinternals", target_dir))

            raise Exception("download failed: " + downUrl)

    class procdump:

        RELEASES_URL = "https://github.com/Sysinternals/ProcDump-for-Linux/releases"

        def latest(self):
            resp = HTTPGET( "/".join([self.RELEASES_URL, "latest"]) )
            tagVer = str(resp.url).split("tag/")[-1]
            return tagVer

        def assets(self, tagVer):
            resp = HTTPGET( "/".join([self.RELEASES_URL, "expanded_assets", tagVer]) )
            assets = re.findall(">(procdump.*?)<", resp.read().decode())
            return assets

        def download(self, tagVer="latest", target_dir='procdump'):
            if "linux" == platform.system().lower():
                if tagVer == "latest": tagVer = self.latest()
                target = self.assets(tagVer)[0]
                downUrl = "/".join([self.RELEASES_URL, "download", tagVer, target])
                resp = HTTPGET(downUrl)
                raise NotImplementedError("linux procdump not implemented")
            else:
                downUrl = "https://download.sysinternals.com/files/Procdump.zip"
                resp = HTTPGET(downUrl)
                if (200 == resp.status):
                    return EXTRACT.zip(resp.read(), target_dir=os.path.join("sysinternals", target_dir))

            raise Exception("download failed: " + downUrl)

    class procmon:

        RELEASES_URL = "https://github.com/Sysinternals/ProcMon-for-Linux/releases"

        def latest(self):
            resp = HTTPGET( "/".join([self.RELEASES_URL, "latest"]) )
            tagVer = str(resp.url).split("tag/")[-1]
            return tagVer

        def assets(self, tagVer):
            resp = HTTPGET( "/".join([self.RELEASES_URL, "expanded_assets", tagVer]) )
            assets = re.findall(">(procmon.*?)<", resp.read().decode())
            return assets

        def download(self, tagVer="latest", target_dir='procmon'):
            if "linux" == platform.system().lower():
                if tagVer == "latest": tagVer = self.latest()
                target = self.assets(tagVer)[0]
                downUrl = "/".join([self.RELEASES_URL, "download", tagVer, target])
                resp = HTTPGET(downUrl)
                raise NotImplementedError("linux procmon not implemented")
            else:
                downUrl = "https://download.sysinternals.com/files/ProcessMonitor.zip"
                resp = HTTPGET(downUrl)
                if (200 == resp.status):
                    return EXTRACT.zip(resp.read(), target_dir=os.path.join("sysinternals", target_dir))

            raise Exception("download failed: " + downUrl)



class dbbrowser:

    class sqlitebrowser:

        RELEASES_URL = "https://github.com/sqlitebrowser/sqlitebrowser/releases"

        def latest(self):
            resp = HTTPGET( "/".join([self.RELEASES_URL, "latest"]) )
            tagVer = str(resp.url).split("tag/")[-1]
            return tagVer

        def assets(self, tagVer):
            resp = HTTPGET( "/".join([self.RELEASES_URL, "expanded_assets", tagVer]) )
            assets = re.findall(">(DB.Browser.for.SQLite-.*?-win64.zip)<", resp.read().decode())
            return assets

        def download(self, tagVer="latest", target_dir='sqlitebrowser'):
            if (os.path.exists(target_dir)): return target_dir

            if tagVer == "latest": tagVer = self.latest()
            target = self.assets(tagVer)[0]
            downUrl = "/".join([self.RELEASES_URL, "download", tagVer, target])
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir=target_dir)

            raise Exception("download failed: " + downUrl)

    class dbeaver:

        RELEASES_URL = "https://github.com/dbeaver/dbeaver/releases"

        def latest(self):
            resp = HTTPGET( "/".join([self.RELEASES_URL, "latest"]) )
            tagVer = str(resp.url).split("/")[-1]
            return tagVer

        def assets(self, tagVer):
            resp = HTTPGET( "/".join([self.RELEASES_URL, "expanded_assets", tagVer]) )
            assets = re.findall(">(dbeaver-ce-.*?.zip)<", resp.read().decode())
            return assets

        def download(self, tagVer="latest", target_dir='dbeaver'):
            if tagVer == "latest": tagVer = self.latest()
            target = self.assets(tagVer)[0]
            downUrl = "/".join([self.RELEASES_URL, "download", tagVer, target])
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir='.')

            raise Exception("download failed: " + downUrl)



class misc:

    class DIEengine:

        RELEASES_URL = "https://github.com/horsicq/DIE-engine/releases"

        def latest(self):
            resp = HTTPGET( "/".join([self.RELEASES_URL, "latest"]) )
            tagVer = str(resp.url).split("tag/")[-1]
            return tagVer

        def assets(self, tagVer):
            resp = HTTPGET( "/".join([self.RELEASES_URL, "expanded_assets", tagVer]) )
            assets = re.findall(f">(die_win64_portable_{tagVer}.*?\.zip)<", resp.read().decode())
            return assets

        def download(self, tagVer="latest", target_dir='die-engine'):
            if tagVer == "latest": tagVer = self.latest()
            target = self.assets(tagVer)[0]
            downUrl = "/".join([self.RELEASES_URL, "download", tagVer, target])
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir=target_dir)

            raise Exception("download failed: " + downUrl)

    class upx:

        RELEASES_URL = "https://github.com/upx/upx/releases"

        def latest(self):
            resp = HTTPGET( "/".join([self.RELEASES_URL, "latest"]) )
            tagVer = str(resp.url).split("tag/")[-1]
            return tagVer

        def assets(self, tagVer):
            resp = HTTPGET( "/".join([self.RELEASES_URL, "expanded_assets", tagVer]) )
            assets = re.findall(">(upx-.*?-win64.zip)<", resp.read().decode())
            return assets

        def download(self, tagVer="latest", target_dir='upx'):
            if tagVer == "latest": tagVer = self.latest()
            target = self.assets(tagVer)[0]
            downUrl = "/".join([self.RELEASES_URL, "download", tagVer, target])
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir='.')

            raise Exception("download failed: " + downUrl)

    class WinObjEx64:

        RELEASES_URL = "https://github.com/hfiref0x/WinObjEx64/releases"

        def latest(self):
            resp = HTTPGET( "/".join([self.RELEASES_URL, "latest"]) )
            tagVer = str(resp.url).split("tag/")[-1]
            return tagVer

        def assets(self, tagVer):
            resp = HTTPGET( "/".join([self.RELEASES_URL, "expanded_assets", tagVer]) )
            assets = re.findall(">(winobjex64.*?.zip)<", resp.read().decode())
            return assets

        def download(self, tagVer="latest", target_dir='WinObjEx64'):
            if tagVer == "latest": tagVer = self.latest()
            target = self.assets(tagVer)[0]
            downUrl = "/".join([self.RELEASES_URL, "download", tagVer, target])
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir=target_dir)

            raise Exception("download failed: " + downUrl)

    class winmerge:

        RELEASES_URL = "https://github.com/WinMerge/winmerge/releases"

        def latest(self):
            resp = HTTPGET( "/".join([self.RELEASES_URL, "latest"]) )
            tagVer = re.findall(r"tag/(.*)", str(resp.url))[0]
            return tagVer

        def assets(self, tagVer):
            resp = HTTPGET( "/".join([self.RELEASES_URL, "expanded_assets", tagVer]) )
            assets = re.findall(">(winmerge-.*?-x64-exe.zip)<", resp.read().decode())
            return assets

        def download(self, tagVer="latest", target_dir='winmerge'):
            if (os.path.exists(target_dir)): return target_dir

            def zipfilter(m:zipfile.ZipInfo):
                if (re.match(r"^WinMerge/", m.filename)):
                    m.filename = re.sub(r"^WinMerge/", "/", m.filename)
                    return True
                return False

            if tagVer == "latest": tagVer = self.latest()
            target = self.assets(tagVer)[0]
            downUrl = "/".join([self.RELEASES_URL, "download", tagVer, target])
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir=target_dir, zipfilter=zipfilter)

            raise Exception("download failed: " + downUrl)

    class Hexer:

        RELEASES_URL = "https://github.com/jovibor/Hexer/releases"

        def latest(self):
            resp = HTTPGET( "/".join([self.RELEASES_URL, "latest"]) )
            tagVer = str(resp.url).split("tag/")[-1]
            return tagVer

        def assets(self, tagVer):
            resp = HTTPGET( "/".join([self.RELEASES_URL, "expanded_assets", tagVer]) )
            assets = re.findall(">(Hexer.exe)<", resp.read().decode())
            return assets

        def download(self, tagVer="latest", target_dir='Hexer'):
            if tagVer == "latest": tagVer = self.latest()
            target = self.assets(tagVer)[0]
            downUrl = "/".join([self.RELEASES_URL, "download", tagVer, target])
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.bin(resp.read(), target_dir='.', target_name=target)

            raise Exception("download failed: " + downUrl)

    class TotalPE2:

        RELEASES_URL = "https://github.com/zodiacon/TotalPE2/releases"

        def latest(self):
            resp = HTTPGET( "/".join([self.RELEASES_URL, "latest"]) )
            tagVer = str(resp.url).split("tag/")[-1]
            return tagVer

        def assets(self, tagVer):
            resp = HTTPGET( "/".join([self.RELEASES_URL, "expanded_assets", tagVer]) )
            assets = re.findall(">(TotalPE.exe)<", resp.read().decode())
            return assets

        def download(self, tagVer="latest", target_dir='TotalPE2'):
            if tagVer == "latest": tagVer = self.latest()
            target = self.assets(tagVer)[0]
            downUrl = "/".join([self.RELEASES_URL, "download", tagVer, target])
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.bin(resp.read(), target_dir=target_dir, target_name=target)

            raise Exception("download failed: " + downUrl)

    class wmie2:

        RELEASES_URL = "https://github.com/chrislogan2/wmie2/releases"

        def latest(self):
            # pre-release
            return "v2.0.1.x"

        def assets(self, tagVer):
            resp = HTTPGET( "/".join([self.RELEASES_URL, "expanded_assets", tagVer]) )
            assets = re.findall(">(WmiExplorer.*?.zip)<", resp.read().decode())
            return assets

        def download(self, tagVer="latest", target_dir='wmie2'):
            if tagVer == "latest": tagVer = self.latest()
            target = self.assets(tagVer)[0]
            downUrl = "/".join([self.RELEASES_URL, "download", tagVer, target])
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir=target_dir)

            raise Exception("download failed: " + downUrl)

    class NamedPipeMaster:

        RELEASES_URL = "https://github.com/zeze-zeze/NamedPipeMaster/releases"

        def latest(self):
            resp = HTTPGET( "/".join([self.RELEASES_URL, "latest"]) )
            tagVer = str(resp.url).split("tag/")[-1]
            return tagVer

        def assets(self, tagVer):
            resp = HTTPGET( "/".join([self.RELEASES_URL, "expanded_assets", tagVer]) )
            assets = re.findall(">(NamedPipeMaster-64bit.zip)<", resp.read().decode())
            return assets

        def download(self, tagVer="latest", target_dir='NamedPipeMaster'):
            if tagVer == "latest": tagVer = self.latest()
            target = self.assets(tagVer)[0]
            downUrl = "/".join([self.RELEASES_URL, "download", tagVer, target])
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir=target_dir)

            raise Exception("download failed: " + downUrl)

    class dnGrep:

        RELEASES_URL = "https://github.com/dnGrep/dnGrep/releases"

        def latest(self):
            resp = HTTPGET( "/".join([self.RELEASES_URL, "latest"]) )
            tagVer = str(resp.url).split("tag/")[-1]
            return tagVer

        def assets(self, tagVer):
            resp = HTTPGET( "/".join([self.RELEASES_URL, "expanded_assets", tagVer]) )
            assets = re.findall(">(dnGrep.*?.x64.zip)<", resp.read().decode())
            return assets

        def download(self, tagVer="latest", target_dir='dnGrep'):
            if tagVer == "latest": tagVer = self.latest()
            target = self.assets(tagVer)[0]
            downUrl = "/".join([self.RELEASES_URL, "download", tagVer, target])
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir=target_dir)

            raise Exception("download failed: " + downUrl)

    class resourcehacker:

        def download(self, target_dir='resourcehacker'):
            downUrl = "http://angusj.com/resourcehacker/resource_hacker.zip"
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir=target_dir)

    class exiftool:

        def download(self, target_dir='exiftool'):
            downUrl = "https://sourceforge.net/projects/exiftool/files/latest/download"
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir=target_dir)

    class trid:

        def download(self, target_dir='trid'):
            downUrl = "http://mark0.net/download/triddefs.zip"
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir=target_dir) \
                    and EXTRACT.zip(HTTPGET("http://mark0.net/download/trid_w32.zip").read(), target_dir=target_dir)

    class winhex:

        def download(self, target_dir='winhex'):
            downUrl = "https://github.com/GTHF/trash_package/raw/main/" \
                "WinHex21.2.zip"
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir=target_dir) \
                    # and self.license(target_dir=target_dir)

        def license(self, target_dir):
            ''' do you have a license? '''
            target = os.path.join(target_dir, "user.txt")
            return target

    class kmdmanager:

        def download(self, target_dir='kmdmanager'):
            downUrl = "https://github.com/GTHF/trash_package/raw/main/KmdManager.exe"
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.bin(resp.read(), target_dir='.', target_name=os.path.basename(resp.url)) \

    class guidedhacking:

        class GHInjector:
            ''' https://github.com/Broihon/GH-Injector-Library/releases '''
            def download(self, target_dir='Injector'):
                ''' https://guidedhacking.com/resources/guided-hacking-dll-injector.4/download '''
                downUrl = "https://github.com/GTHF/trash_package/raw/main/GH/GH%20Injector.zip"
                resp = HTTPGET(downUrl)
                if (200 == resp.status):
                    return EXTRACT.zip(resp.read(), target_dir=os.path.join("GH", target_dir))

        class GHCheatEngine:
            ''' https://github.com/cheat-engine/cheat-engine/releases '''
            def download(self, target_dir='AesopEngine'):
                ''' https://guidedhacking.com/resources/gh-undetected-cheat-engine-download-udce-driver.14/download '''
                downUrl = "https://github.com/GTHF/trash_package/raw/main/GH/AesopEngine.zip"
                resp = HTTPGET(downUrl)
                if (200 == resp.status):
                    UEDumperUrl = "https://github.com/GTHF/trash_package/raw/main/GH/GH_UE_Dumper.zip"
                    return EXTRACT.zip(HTTPGET(UEDumperUrl).read(), target_dir=os.path.join("GH", "AesopEngine")) and \
                        EXTRACT.zip(resp.read(), target_dir=os.path.join("GH", "."))

    class zoomit:
        def download(self, target_dir='zoomit'):
            downUrl = "https://download.sysinternals.com/files/ZoomIt.zip"
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir=target_dir)

            raise Exception("download failed: " + downUrl)



class winark:
    ''' Windows Anti-Rootkit '''

    class systeminformer:

        RELEASES_URL = "https://github.com/winsiderss/si-builds/releases"

        def latest(self):
            resp = HTTPGET( "/".join([self.RELEASES_URL, "latest"]) )
            tagVer = str(resp.url).split("tag/")[-1]
            return tagVer

        def assets(self, tagVer):
            resp = HTTPGET( "/".join([self.RELEASES_URL, "expanded_assets", tagVer]) )
            assets = re.findall(">(systeminformer.*?release-bin.zip)<", resp.read().decode())
            return assets

        def download(self, tagVer="latest", target_dir='systeminformer'):
            if tagVer == "latest": tagVer = self.latest()
            target = self.assets(tagVer)[0]
            downUrl = "/".join([self.RELEASES_URL, "download", tagVer, target])
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir=target_dir)

            raise Exception("download failed: " + downUrl)

    class WinArk:

        RELEASES_URL = "https://github.com/BeneficialCode/WinArk/releases"

        def latest(self):
            resp = HTTPGET( "/".join([self.RELEASES_URL, "latest"]) )
            tagVer = str(resp.url).split("tag/")[-1]
            return tagVer

        def assets(self, tagVer):
            resp = HTTPGET( "/".join([self.RELEASES_URL, "expanded_assets", tagVer]) )
            assets = re.findall(">(WinArk.zip)<", resp.read().decode())
            return assets

        def download(self, tagVer="latest", target_dir='winark'):
            if tagVer == "latest": tagVer = self.latest()
            target = self.assets(tagVer)[0]
            downUrl = "/".join([self.RELEASES_URL, "download", tagVer, target])
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir=os.path.join(target_dir))

            raise Exception("download failed: " + downUrl)

    class WKE:
        def download(self, target_dir='winark'):
            downUrl = "https://github.com/AxtMueller/Windows-Kernel-Explorer" \
                "/archive/" "master" ".zip"
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir=target_dir)

    class WKTools:
        def download(self, target_dir='winark'):
            downUrl = "https://github.com/AngleHony/WKTools" \
                "/blob/main/WKTools.exe?raw=true"
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.bin(resp.read(), target_dir=os.path.join(target_dir, "WKTools"), target_name=os.path.basename(resp.url))

    class Pyark:
        def download(self, target_dir='winark'):
            downUrl = "https://github.com/antiwar3/py" \
                "/blob/master/Pyark.zip?raw=true"
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir=os.path.join(target_dir, "pyark"))

    class YDArk:
        ''' driver file not signed '''
        def download(self, target_dir='winark'):
            # downUrl = "https://github.com/ClownQq/YDArk" \
            #     "/archive/" "master" ".zip"
            downUrl = "https://github.com/GTHF/trash_package/raw/main/" \
                "YDArk-1.0.3.3-signed.zip"
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir=os.path.join(target_dir, "YDArk"))



if __name__ == "__main__":

    x64DBG = debugger.x64dbg().download(); \
        misc.DIEengine().download(); \
        misc.upx().download(); \
        misc.winhex().download(); \
        misc.guidedhacking.GHInjector().download(); \
        misc.guidedhacking.GHCheatEngine().download(); \
        misc.resourcehacker().download(); \
        misc.winmerge().download(); \
        dbbrowser.sqlitebrowser().download(); \

    dumper.ksdumper().download(); \
        dumper.winchecksec().download(); \
        dumper.pe_sieve().download(); \
        # dumper.binskim().download(); \

    winark.systeminformer().download(); \
        winark.WKE().download(); \
        winark.Pyark().download(); \
        winark.WKTools().download(); \
        winark.YDArk().download(); \

    sysinternals.procmon().download(); \
        sysinternals.procexp().download(); \
        sysinternals.pstools().download(); \
        sysinternals.sysmon().download(); \
        sysinternals.winobj().download(); \
        sysinternals.debugview().download(); \

    # if (input("plug-in download? (y/n):").lower().startswith("y")):
    #     debugger.x64dbg.plugin(x64DBG)