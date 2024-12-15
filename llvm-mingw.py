#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, io, sys, re, types, platform, subprocess, urllib.request

HTTPGET = urllib.request.urlopen

if not bool(os.environ.get("DEBUGPY_RUNNING")):
    target = "utils/common"
    RAW_CODE = HTTPGET(f"https://github.com/nblog/cloud-py3-example/blob/main/{target}.py?raw=true").read().decode('utf-8')

    raw_module = types.ModuleType('common')
    sys.modules['utils.common'] = raw_module
    exec(RAW_CODE, raw_module.__dict__)

from utils.common import (
    EXTRACT, GITHUB_RELEASES
)


class llvm_mingw:
    ''' https://github.com/mstorsjo/llvm-mingw/releases '''

    TARGET_CRT = "msvcrt-x86_64" or "ucrt-x86_64" or "ucrt-aarch64"

    def download(self, target_dir="llvm-mingw-x86_64", tagVer="latest"):
        downUrl = GITHUB_RELEASES(source="mstorsjo/llvm-mingw").geturl(f"llvm-mingw-.*?-{llvm_mingw.TARGET_CRT}\.zip", tagVer)
        resp = HTTPGET(downUrl)
        if (200 == resp.status):
            return EXTRACT.zip(resp.read(), target_dir=target_dir)

        raise Exception("download failed: " + downUrl)



if __name__ == "__main__":

    if 'windows' != platform.system().lower():
        raise NotImplementedError("only support windows")

    toolchain = llvm_mingw().download()

    if (input("install environment variables to the system? (y/n):").lower().startswith("y")):
        import winreg

        # ''' HKEY_CURRENT_USER\Environment '''
        # with winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER) as hkey:
        #     with winreg.OpenKey(hkey, r"Environment", 0, winreg.KEY_ALL_ACCESS) as subkey:
        #         path = winreg.QueryValueEx(subkey, "Path")[0]
        #         if toolchain not in path:
        #             winreg.SetValueEx(subkey, "Path", 0, winreg.REG_EXPAND_SZ, ';'.join([path, os.path.join(toolchain, 'bin'), toolchain]))
        #             print(f"add \"{toolchain}\\bin\" and \"{toolchain}\" to the environment variable")

        ''' HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment '''
        with winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE) as hkey:
            with winreg.OpenKey(hkey, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment", 0, winreg.KEY_ALL_ACCESS) as subkey:
                path = winreg.QueryValueEx(subkey, "Path")[0]
                if toolchain not in path:
                    winreg.SetValueEx(subkey, "Path", 0, winreg.REG_EXPAND_SZ, ';'.join([path, os.path.join(toolchain, 'bin'), toolchain]))
                    print(f"add \"{toolchain}\\bin\" and \"{toolchain}\" to the environment variable")