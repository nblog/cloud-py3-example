#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, re, platform, urllib.request, subprocess


HTTPGET = urllib.request.urlopen


print( "warn: `embeddable` not supported" )


from multiprocessing import Process

class DynamicPip:

    @staticmethod
    def has_pip():
        return 0 == \
            subprocess.call([sys.executable, "-m", "pip", "--version"])

    @staticmethod
    def pip():
        def ensurepip():
            from tempfile import TemporaryFile
            with TemporaryFile("wb", delete=False) as fp:
                open(fp.name, "wb").write(HTTPGET("https://bootstrap.pypa.io/get-pip.py").read())
                fp.close(); return fp.name

        proc = Process(target=subprocess.check_call,
                args=([sys.executable, ensurepip()]))
        proc.start(); proc.join()

    @staticmethod
    def install(packages: list, indexurl: str):
        if 0 == len(packages): return

        pipcmd = [sys.executable, "-m", "pip", "install"] + packages
        if indexurl: pipcmd.extend(["-i", indexurl])

        subprocess.check_call(pipcmd, shell=True)



if __name__ == "__main__":
    ''' install pip '''
    if not DynamicPip.has_pip(): DynamicPip.pip()

    packages = list(filter(len, os.environ.get("PIP_INSTALL_PACKAGES", '').split(' ')))
    DynamicPip.install(packages, os.environ.get("PIP_INDEX_URL", ''))

    '''
        similar to the 'pywin32' library, 
        there are `.pth` files, 
        you need to reset the environment to let it initialize the paths.
    '''
    import importlib, site
    importlib.reload(site)