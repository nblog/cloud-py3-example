#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, io, sys, re, types, platform, subprocess, urllib.request

HTTPGET = urllib.request.urlopen

if not bool(os.environ.get("DEBUGPY_RUNNING")):
    target = "utils/common"
    DOWNURL = f"https://github.com/nblog/cloud-py3-example/blob/main/{target}.py?raw=true"
    exec(HTTPGET(DOWNURL).read().decode('utf-8'))

from utils.common import (
    EXTRACT, GITHUB_RELEASES
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
            downUrl = GITHUB_RELEASES(source="frida/frida").geturl(f"frida-gadget-.*?-{frida.TARGET.system}-{frida.TARGET.arch}.*?\.xz", tagVer)
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.xz(resp.read(), target_dir=target_dir, target_name=os.path.basename(downUrl))

    class frida_server:
        def download(self, target_dir="frida-server", tagVer="latest"):
            downUrl = GITHUB_RELEASES(source="frida/frida").geturl(f"frida-server-.*?-{frida.TARGET.system}-{frida.TARGET.arch}.*?\.xz", tagVer)
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                return EXTRACT.xz(resp.read(), target_dir=target_dir, target_name=os.path.basename(downUrl))

        def run(self, argv=[], binpath=''):
            self.app = subprocess.Popen([binpath]+argv)



if __name__ == "__main__":

    FRIDA_VERSION = os.environ.get("FRIDA_VERSION", "latest")

    ''' default listen: all ipv4 (0.0.0.0:27042)  all ipv6 (::) '''
    FRIDA_SERVER_PORT = os.environ.get("FRIDA_SERVER_PORT", "27042")

    cmd = ["--listen", ':'.join(["0.0.0.0", FRIDA_SERVER_PORT])]

    if ("FRIDA_SERVER_TOKEN" in os.environ):
        cmd += ["--token", os.environ["FRIDA_SERVER_TOKEN"]]

    app = frida.frida_server(); app.run(cmd, app.download(tagVer=FRIDA_VERSION))

    ''' reserved for frpc '''
    os.environ["FRPC_LOCAL_PORT"] = FRIDA_SERVER_PORT