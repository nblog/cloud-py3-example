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
                member.filename = os.path.basename(member.filename)
                archive.extract(member, target_dir)
        return os.path.join(os.getcwd(), target_dir)

    @staticmethod
    def tar(data, target_dir):
        import io, tarfile
        tarfile.open(fileobj=io.BytesIO(data)).extractall(target_dir)
        return os.path.join(os.getcwd(), target_dir)



class dumper:

    class binskim:

        RELEASES_URL = "https://github.com/microsoft/binskim/releases"

        def latest(self):
            resp = HTTPGET( "/".join([self.RELEASES_URL, "latest"]) )
            tagVer = str(resp.url).split("tag/")[-1]
            return tagVer

        def download(self, tagVer="latest", target_dir='binskim'):
            if tagVer == "latest": tagVer = self.latest()

            downUrl = \
                "https://www.nuget.org/api/v2/package/Microsoft.CodeAnalysis.BinSkim/{0}".format(tagVer[1:])
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(
                    resp.read(), 
                    target_dir=target_dir, zipfilter=lambda x: x.filename.startswith("tools/netcoreapp3.1/win"))

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
            downUrl = "/".join([self.RELEASES_URL, "download", tagVer, target])
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir=target_dir)

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

    class pe_unmapper:

        RELEASES_URL = "https://github.com/hasherezade/pe_unmapper/releases"

        def latest(self):
            resp = HTTPGET( "/".join([self.RELEASES_URL, "latest"]) )
            tagVer = str(resp.url).split("tag/")[-1]
            return tagVer

        def assets(self, tagVer):
            resp = HTTPGET( "/".join([self.RELEASES_URL, "expanded_assets", tagVer]) )
            assets = re.findall(">(pe_unmapper.zip)<", resp.read().decode())
            return assets

        def download(self, tagVer="latest", target_dir='pe_unmapper'):
            if tagVer == "latest": tagVer = self.latest()
            target = self.assets(tagVer)[0]
            downUrl = "/".join([self.RELEASES_URL, "download", tagVer, target])
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir=target_dir)

            raise Exception("download failed: " + downUrl)

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
            return EXTRACT.zip(resp.read(), target_dir=target_dir) \
            and self.plugin(target_dir)

        raise Exception("download failed: " + downUrl)

    def plugin(self, target_dir='x64dbg'):
        ''' x64dbg plugin '''
        def ClawSearch(target_dir):
            ''' https://github.com/codecat/ClawSearch/releases/latest '''

        def OllyDumpEx(target_dir):
            ''' https://low-priority.appspot.com/ollydumpex/OllyDumpEx.zip '''

        def Multiline_Ultimate_Assembler(target_dir):
            ''' https://ramensoftware.com/downloads/multiasm.rar '''

        def SharpOD(target_dir):
            ''' https://down.52pojie.cn/Tools/OllyDbg_Plugin/SharpOD_x64_v0.6d_Stable.zip '''

        return None \
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



class systeminformer:

    RELEASES_URL = "https://github.com/winsiderss/systeminformer/releases"

    def latest(self):
        resp = HTTPGET( "/".join([self.RELEASES_URL, "latest"]) )
        tagVer = str(resp.url).split("tag/")[-1]
        return tagVer

    def assets(self, tagVer):
        resp = HTTPGET( "/".join([self.RELEASES_URL, "expanded_assets", tagVer]) )
        assets = re.findall(">(SystemInformer.*?.zip)<", resp.read().decode())
        return assets

    def download(self, tagVer="latest", target_dir='systeminformer'):
        if tagVer == "latest": tagVer = self.latest()
        target = self.assets(tagVer)[0]
        downUrl = "/".join([self.RELEASES_URL, "download", tagVer, target])
        resp = HTTPGET(downUrl)
        if (200 == resp.status):
            return EXTRACT.zip(resp.read(), target_dir=target_dir)

        raise Exception("download failed: " + downUrl)



class die_engine:

    RELEASES_URL = "https://github.com/horsicq/DIE-engine/releases"

    def latest(self):
        resp = HTTPGET( "/".join([self.RELEASES_URL, "latest"]) )
        tagVer = str(resp.url).split("tag/")[-1]
        return tagVer

    def assets(self, tagVer):
        resp = HTTPGET( "/".join([self.RELEASES_URL, "expanded_assets", tagVer]) )
        assets = re.findall(f">(die_win64_portable_{tagVer}?.zip)<", resp.read().decode())
        return assets

    def download(self, tagVer="latest", target_dir='die-engine'):
        if tagVer == "latest": tagVer = self.latest()
        target = self.assets(tagVer)[0]
        downUrl = "/".join([self.RELEASES_URL, "download", tagVer, target])
        resp = HTTPGET(downUrl)
        if (200 == resp.status):
            return EXTRACT.zip(resp.read(), target_dir=target_dir)

        raise Exception("download failed: " + downUrl)



class sysinternals:

    class debugview:
        def download(self, target_dir='debugview'):
            downUrl = "https://download.sysinternals.com/files/DebugView.zip"
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



class misc:

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
            if tagVer == "latest": tagVer = self.latest()
            target = self.assets(tagVer)[0]
            downUrl = "/".join([self.RELEASES_URL, "download", tagVer, target])
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir='.')

            raise Exception("download failed: " + downUrl)

    class resourcehacker:

        def download(self, target_dir='resourcehacker'):
            downUrl = "http://angusj.com/resourcehacker/resource_hacker.zip"
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir=target_dir)



class winark:
    ''' Windows Anti-Rootkit '''

    class WKE:
        def download(self, target_dir='ark'):
            downUrl = "https://github.com/AxtMueller/Windows-Kernel-Explorer" \
                "/archive/" "master" ".zip"
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir=target_dir)

    class WKTools:
        def download(self, target_dir='ark'):
            downUrl = "https://github.com/AngleHony/WKTools" \
                "/archive/" "main" ".zip"
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir=target_dir)

    class ke64:
        def download(self, target_dir='ark'):
            downUrl = "https://github.com/alinml/ke64" \
                "/blob/main/ke64.zip?raw=true"
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir=os.path.join(target_dir, "ke64"))

    class pyark:
        def download(self, target_dir='ark'):
            downUrl = "https://github.com/antiwar3/py" \
                "/blob/master/Pyark.zip?raw=true"
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir=os.path.join(target_dir, "pyark"))



if __name__ == "__main__":

    # dumper.binskim().download(), \

    misc.upx().download(), \

    x64dbg().download(), \
        die_engine().download(), \

    winark.WKE().download(), \
        winark.WKTools().download(), \
        winark.ke64().download(), \
        winark.pyark().download(), \


    sysinternals.debugview().download(), \
        sysinternals.sysmon().download(), \
        sysinternals.procmon().download()