#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, re, platform, urllib.request, subprocess


HTTPGET = urllib.request.urlopen


class EXTRACT:

    @staticmethod
    def zip(data, target_dir):
        import io, zipfile
        zipfile.ZipFile(io.BytesIO(data)).extractall(target_dir)
        return os.path.join(os.getcwd(), target_dir)

    @staticmethod
    def tar(data, target_dir):
        import io, tarfile
        tarfile.open(fileobj=io.BytesIO(data)).extractall(target_dir)
        return os.path.join(os.getcwd(), target_dir)



class dumper:

    class pe_unmapper:

        RELEASES_URL = os.environ.get("GHPROXY","") + \
            "https://github.com/hasherezade/pe_unmapper/releases"


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

    class pe_sieve:

        RELEASES_URL = os.environ.get("GHPROXY","") + \
            "https://github.com/hasherezade/pe-sieve/releases"


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

    class ksdumper:

        RELEASES_URL = os.environ.get("GHPROXY","") + \
            "https://github.com/mastercodeon314/KsDumper-11/releases"


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

    class winchecksec:

        RELEASES_URL = os.environ.get("GHPROXY","") + \
            "https://github.com/trailofbits/winchecksec/releases"


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



class x64dbg:

    RELEASES_URL = os.environ.get("GHPROXY","") + \
        "https://github.com/x64dbg/x64dbg/releases"


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

    def plugin(self):
        ''' x64dbg plugin '''
        '''
        https://down.52pojie.cn/Tools/OllyDbg_Plugin/SharpOD_x64_v0.6d_Stable.zip
        https://low-priority.appspot.com/ollydumpex/OllyDumpEx.zip
        https://github.com/fjqisba/E-Debug/releases

        https://ramensoftware.com/downloads/multiasm.rar
        https://github.com/codecat/ClawSearch/releases/latest
        '''
        raise NotImplementedError



class systeminformer:

    RELEASES_URL = os.environ.get("GHPROXY","") + \
        "https://github.com/winsiderss/systeminformer/releases"


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

    RELEASES_URL = os.environ.get("GHPROXY","") + \
        "https://github.com/horsicq/DIE-engine/releases"


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



class upx:

    RELEASES_URL = os.environ.get("GHPROXY","") + \
        "https://github.com/upx/upx/releases"


    def latest(self):
        resp = HTTPGET( "/".join([self.RELEASES_URL, "latest"]) )
        tagVer = str(resp.url).split("tag/")[-1]
        return tagVer

    def assets(self, tagVer):
        resp = HTTPGET( "/".join([self.RELEASES_URL, "expanded_assets", tagVer]) )
        assets = re.findall(">(upx-.*?-win64.zip)<", resp.read().decode())
        return assets

    def download(self, tagVer="latest", target_dir='.'):
        if tagVer == "latest": tagVer = self.latest()
        target = self.assets(tagVer)[0]
        downUrl = "/".join([self.RELEASES_URL, "download", tagVer, target])
        resp = HTTPGET(downUrl)
        if (200 == resp.status):
            return EXTRACT.zip(resp.read(), target_dir=target_dir)

        raise Exception("download failed: " + downUrl)



class sqlitebrowser:

    RELEASES_URL = os.environ.get("GHPROXY","") + \
        "https://github.com/sqlitebrowser/sqlitebrowser/releases"


    def latest(self):
        resp = HTTPGET( "/".join([self.RELEASES_URL, "latest"]) )
        tagVer = str(resp.url).split("tag/")[-1]
        return tagVer

    def assets(self, tagVer):
        resp = HTTPGET( "/".join([self.RELEASES_URL, "expanded_assets", tagVer]) )
        assets = re.findall(">(DB.Browser.for.SQLite-.*?-win64.zip)<", resp.read().decode())
        return assets

    def download(self, tagVer="latest", target_dir='.'):
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

    class procdump:

        RELEASES_URL = os.environ.get("GHPROXY","") + \
            "https://github.com/Sysinternals/ProcDump-for-Linux/releases"


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



class misc:

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
            downUrl = os.environ.get("GHPROXY","") + \
                "https://github.com/AxtMueller/Windows-Kernel-Explorer" \
                "/archive/refs/heads/master.zip"
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir=target_dir)

    class WKTools:
        def download(self, target_dir='ark'):
            downUrl = os.environ.get("GHPROXY","") + \
                "https://github.com/AngleHony/WKTools" \
                "/archive/refs/heads/main.zip"
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.zip(resp.read(), target_dir=target_dir)



if __name__ == "__main__":

    x64dbg().download()

    die_engine().download()

    winark.WKE().download(); winark.WKTools().download()


    sysinternals.debugview().download()
