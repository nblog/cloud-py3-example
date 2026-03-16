#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, io, sys, re, platform, subprocess

from cloud_py3._common import EXTRACT, GITHUB_RELEASES, download2


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


def main():
    ''' to execute, runas `administrator` '''
    from cloud_py3.has_root import has_root, main as has_root_main
    os.environ.setdefault("HAS_ROOT", "1")
    has_root_main()

    ''' default listen: all ipv4 (0.0.0.0:27042)  all ipv6 (::) '''
    FRIDA_SERVER_PORT = os.getenv("FRIDA_SERVER_PORT", "27042")

    cmd = ["--listen", ':'.join(["0.0.0.0", FRIDA_SERVER_PORT])]

    if ("FRIDA_SERVER_TOKEN" in os.environ):
        cmd += ["--token", os.environ["FRIDA_SERVER_TOKEN"]]

    app = frida.frida_server(); app.run(cmd, app.download(tagVer=os.getenv("FRIDA_VERSION", "latest")))

    os.environ["EXEC_LOCAL_PORT"] = FRIDA_SERVER_PORT


if __name__ == "__main__":
    main()
