#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, io, sys, re, types, platform, subprocess, urllib.request

HTTPGET = urllib.request.urlopen

if not bool(os.environ.get("DEBUGPY_RUNNING")):
    source = "utils/common"
    RAW_CODE = HTTPGET(f"https://github.com/nblog/cloud-py3-example/blob/main/{source}.py?raw=true").read().decode('utf-8')

    raw_module = types.ModuleType(source.split('/')[-1])
    sys.modules[source.replace('/', '.')] = raw_module
    exec(RAW_CODE, raw_module.__dict__)

from utils.common import (
    EXTRACT, GITHUB_RELEASES, download2
)


class frida:
    ''' https://github.com/frida/frida/releases '''

    class TARGET:
        system = dict({
            "darwin": "macos",
        }).get(platform.system().lower(), platform.system().lower())
        arch = dict({
            "i386": "x86",
            "amd64": "x86_64",
        }).get(platform.machine().lower(), platform.machine().lower())

    class frida_gadget:
        def download(self, target_dir="frida-gadget", tagVer="latest"):
            downUrl = GITHUB_RELEASES(source="frida/frida").geturl(f"frida-gadget-.*?-{frida.TARGET.system}-{frida.TARGET.arch}.*?.xz", tagVer)
            return EXTRACT.xz(download2(downUrl), target_dir=target_dir, target_name=os.path.basename(downUrl))

    class frida_server:
        def download(self, target_dir="frida-server", tagVer="latest"):
            downUrl = GITHUB_RELEASES(source="frida/frida").geturl(f"frida-server-.*?-{frida.TARGET.system}-{frida.TARGET.arch}.*?.xz", tagVer)
            return EXTRACT.xz(download2(downUrl), target_dir=target_dir, target_name=os.path.basename(downUrl))

        def run(self, argv=[], binpath=''):
            self.app = subprocess.Popen([binpath]+argv)



if __name__ == "__main__":

    ''' to execute, runas `administrator` '''
    os.environ.setdefault("HAS_ROOT", "1")
    DOWNURL = f"https://github.com/nblog/cloud-py3-example/blob/main/has-root.py?raw=true"
    exec(HTTPGET(DOWNURL).read().decode('utf-8'))


    ''' default listen: all ipv4 (0.0.0.0:27042)  all ipv6 (::) '''
    FRIDA_SERVER_PORT = os.getenv("FRIDA_SERVER_PORT", "27042")

    cmd = ["--listen", ':'.join(["0.0.0.0", FRIDA_SERVER_PORT])]

    if ("FRIDA_SERVER_TOKEN" in os.environ):
        cmd += ["--token", os.environ["FRIDA_SERVER_TOKEN"]]

    app = frida.frida_server(); app.run(cmd, app.download(tagVer=os.getenv("FRIDA_VERSION", "latest")))

    os.environ["EXEC_LOCAL_PORT"] = FRIDA_SERVER_PORT