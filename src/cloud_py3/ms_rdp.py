#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, pathlib, platform, subprocess

from cloud_py3._common import HTTPGET, EXTRACT, GITHUB_RELEASES


class rdpwrap:
    ''' ⚠ warn: will be alerted to viruses ⚠ '''
    ''' https://github.com/sebaxakerhtc/rdpwrap/releases/latest '''
    ''' https://github.com/sebaxakerhtc/rdpwrap.ini '''

    RDP_DIRECTORY = os.path.expandvars(os.path.join(r"$ProgramFiles", "RDP Wrapper"))

    def enable_blank_password(self, enable=True):
        import winreg
        value = 0 if enable else 1
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                            r"System\CurrentControlSet\Control\Lsa", 
                            0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, "LimitBlankPasswordUse", 0, winreg.REG_DWORD, value)

    def download(self, target_dir=".", tagVer="latest"):
        if not os.path.exists(self.RDP_DIRECTORY):
            os.makedirs(self.RDP_DIRECTORY, exist_ok=True)

        # add exclusion `Windows Defender`
        subprocess.run(["powershell", "-Command", 
            f"Add-MpPreference -ExclusionPath '{self.RDP_DIRECTORY}'"], 
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        downUrl = GITHUB_RELEASES(source="sebaxakerhtc/rdpwrap").geturl(f"RDPW_Installer.exe", tagVer)
        resp = HTTPGET(downUrl)
        if (200 == resp.status):
            return EXTRACT.bin(resp.read(), target_dir=self.RDP_DIRECTORY, target_name=os.path.basename(downUrl))

        raise Exception("download failed: " + downUrl)

    def run(self, argv=[], binpath=''):
        subprocess.run([binpath, *argv], cwd=self.RDP_DIRECTORY)


def main():
    if 'windows' != platform.system().lower():
        raise NotImplementedError("only support windows")

    # ''' runas `administrator` '''
    # from cloud_py3.has_root import has_root, main as has_root_main
    # os.environ.setdefault("HAS_ROOT", "1")
    # has_root_main()

    # rdp = rdpwrap()
    # rdp.download(); rdp.run()

    MSRDP_PORT = '3389'
    os.environ["EXEC_LOCAL_PORT"] = MSRDP_PORT


if __name__ == "__main__":
    main()
