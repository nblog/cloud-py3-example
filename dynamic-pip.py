#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, platform, urllib.request, subprocess


HTTPGET = urllib.request.urlopen


import sys; from multiprocessing import Process

class DynamicPip:

    @staticmethod
    def has_pip():
        return not b'No module named pip' in \
            subprocess.check_output(
            [sys.executable, "-m", "pip", "--version"], stderr=subprocess.STDOUT)

    @staticmethod
    def pip():
        def ensurepip():
            from tempfile import mkstemp; fd, name = mkstemp()
            open(name, "wb").write(HTTPGET("https://bootstrap.pypa.io/get-pip.py").read())
            return name
        p = Process(target=subprocess.check_call,
                args=([sys.executable, ensurepip()],))
        p.start(); p.join()

    @staticmethod
    def install(packages:list, indexurl=None):
        pipcmd=[sys.executable, "-m", "pip", "install"] + packages
        if indexurl: pipcmd.extend(["-i", indexurl])
        subprocess.check_call(pipcmd)



if __name__ == "__main__":
    ''' install pip '''
    if not DynamicPip.has_pip(): DynamicPip.pip()
    packages = list(filter(len, os.environ.get("PIP_INSTALL_PACKAGES").split(" ")))
    DynamicPip.install(packages, os.environ.get("PIP_INDEX_URL"))