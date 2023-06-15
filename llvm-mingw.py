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
                archive.extract(member, target_dir)
        return os.path.join(os.getcwd(), target_dir)


class llvm_mingw:

    RELEASES_URL = "https://github.com/mstorsjo/llvm-mingw/releases"

    def latest(self):
        resp = HTTPGET( "/".join([self.RELEASES_URL, "latest"]) )
        tagVer = str(resp.url).split("tag/")[-1]
        return tagVer

    def assets(self, tagVer):
        resp = HTTPGET( "/".join([self.RELEASES_URL, "expanded_assets", tagVer]) )
        assets = re.findall(">(llvm-mingw-.*?-msvcrt-x86_64.zip)<", resp.read().decode())
        return assets

    def download(self, tagVer="latest", target_dir='llvm-mingw-x86_64'):
        if tagVer == "latest": tagVer = self.latest()
        target = self.assets(tagVer)[0]
        downUrl = "/".join([self.RELEASES_URL, "download", tagVer, target])
        resp = HTTPGET(downUrl)
        if (200 == resp.status):
            return EXTRACT.zip(resp.read(), target_dir=target_dir)

        raise Exception("download failed: " + downUrl)



if __name__ == "__main__":

    if 'windows' != platform.system().lower():
        raise NotImplementedError("only support windows")

    toolchain = llvm_mingw().download()

    c = input("install environment variables to the system? (y/n):")
    if ('y' == c.lower()[0]):
        import winreg

        ''' HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment '''
        with winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE) as hkey:
            with winreg.OpenKey(hkey, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment", 0, winreg.KEY_ALL_ACCESS) as subkey:
                path = winreg.QueryValueEx(subkey, "Path")[0]
                if toolchain not in path:
                    winreg.SetValueEx(subkey, "Path", 0, winreg.REG_EXPAND_SZ, ';'.join([path, os.path.join(toolchain, 'bin'), toolchain]))
                    print(f"add \"{toolchain}\\bin\" and \"{toolchain}\" to the environment variable")