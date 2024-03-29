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

    @staticmethod
    def tar(data, target_dir):
        import io, tarfile
        tarfile.open(fileobj=io.BytesIO(data)).extractall(target_dir)
        return os.path.join(os.getcwd(), target_dir)

    @staticmethod
    def bin(data, target_dir, target_name):
        target = os.path.join(target_dir, target_name)
        os.makedirs(target_dir, exist_ok=True)
        open(target, "wb").write(data)
        return target



def update_win7sp1():
    KB976932 = "https://catalog.s.download.windowsupdate.com/msdownload/update/software/svpk/2011/02/windows6.1-kb976932-x64_74865ef2562006e51d7f9333b4a8d45b7a749dab.exe"
    return


class PATCHes:

    @staticmethod
    def DOTNET():
        REBOOT = False
        if (0 == len(re.findall("Windows-7-[0-9\.]+-SP1", platform.platform()))):
            return REBOOT
        if (0 == subprocess.call( \
            "systeminfo | FIND \"KB2813430\"", shell=True, stdout=subprocess.PIPE)):
            return REBOOT

        KB2813430 = "http://download.windowsupdate.com/d/msdownload/update/software/secu/2013/05/windows6.1-kb2813430-x64_0a282a6077331c034ba2d31b85dfe65dcc71e380.msu"
        resp = HTTPGET(KB2813430)
        if (200 == resp.status):
            target = EXTRACT.bin(resp.read(), os.getcwd(), os.path.basename(resp.url))
            print(f"please install the {target}."); REBOOT = True

        return REBOOT

    @staticmethod
    def SHA2():
        REBOOT = False
        if (0 == len(re.findall("Windows-7-[0-9\.]+-SP1", platform.platform()))):
            return REBOOT
        if (0 == subprocess.call( \
            "systeminfo | FIND \"KB4474419\"", shell=True, stdout=subprocess.PIPE)):
            return REBOOT
        if (0 == subprocess.call( \
            "systeminfo | FIND \"KB4490628\"", shell=True, stdout=subprocess.PIPE)):
            return REBOOT

        KB4474419 = "http://download.windowsupdate.com/c/msdownload/update/software/secu/2019/09/windows6.1-kb4474419-v3-x64_b5614c6cea5cb4e198717789633dca16308ef79c.msu"
        resp = HTTPGET(KB4474419)
        if (200 == resp.status):
            target = EXTRACT.bin(resp.read(), os.getcwd(), os.path.basename(resp.url))
            print(f"please install the {target}."); REBOOT = True

        KB4490628 = "http://download.windowsupdate.com/c/msdownload/update/software/secu/2019/03/windows6.1-kb4490628-x64_d3de52d6987f7c8bdc2c015dca69eac96047c76e.msu"
        resp = HTTPGET(KB4490628)
        if (200 == resp.status):
            target = EXTRACT.bin(resp.read(), os.getcwd(), os.path.basename(resp.url))
            print(f"please install the {target}."); REBOOT = True

        return REBOOT


''' https://download.microsoft.com/download/C/8/7/C87AE67E-A228-48FB-8F02-B2A9A1238099/Windows6.1-KB3033929-x64.msu '''



if __name__ == "__main__":
    raise NotImplementedError("hasn't been implemented yet...")