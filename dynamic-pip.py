#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, platform, urllib.request, subprocess


HTTPGET = urllib.request.urlopen


class DynamicPip:

    @staticmethod
    def has_pip():
        import sys
        try: return 0 == subprocess.check_call([sys.executable, "-m", "pip", "--version"])
        except: return False

    @staticmethod
    def pip():
        from multiprocessing import Process
        DOWNURL = "https://bootstrap.pypa.io/get-pip.py"
        Process(target=exec, args=(HTTPGET(DOWNURL).read().decode('utf-8'),)).start()

    @staticmethod
    def install(packages:list, indexurl=None):
        import sys; from multiprocessing import Process
        pipcmd=[sys.executable, "-m", "pip", "install"] + packages
        if indexurl: pipcmd.extend(["-i", indexurl])
        Process(target=subprocess.check_call, 
                args=(pipcmd,)).start()



if __name__ == "__main__":
    ''' install pip '''
    if not DynamicPip.has_pip(): DynamicPip.pip()
    packages = list(filter(len, os.environ.get("PIP_INSTALL_PACKAGES").split(" ")))
    DynamicPip.install(packages, os.environ.get("PIP_INDEX_URL"))