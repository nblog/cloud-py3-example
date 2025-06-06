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
    EXTRACT, GITHUB_RELEASES
)


class nodepass:
    ''' https://github.com/yosebyte/nodepass/releases '''

    class TARGET:
        system = platform.system().lower()
        arch = dict({
            "x86_64": "amd64", 
            "armv8l": "arm64", "aarch64": "arm64", 
        }).get(platform.machine().lower(), platform.machine().lower())

    def download(self, target_dir="nodepass", tagVer="latest"):
        downUrl = GITHUB_RELEASES(source="yosebyte/nodepass").geturl(f"nodepass_.*?_{nodepass.TARGET.system}_{nodepass.TARGET.arch}.*?", tagVer)
        resp = HTTPGET(downUrl)
        if (200 == resp.status):
            return EXTRACT.extract(resp.read(), target_dir=target_dir)
        raise Exception("download failed: " + downUrl)

    def run(self, argv=[], target_dir="."):
        binpath = os.path.abspath(os.path.join(target_dir, "nodepass"))
        self.app = subprocess.Popen([binpath]+argv)



if __name__ == "__main__":

    if "NP_SERVER_ADDRESS" not in os.environ \
        or "NP_SERVER_PORT" not in os.environ:
        print("error:",
            " `NP_SERVER_ADDRESS`"
            " `NP_SERVER_PORT`"
            " must be set\n"); exit(1)

    if "EXEC_LOCAL_PORT" in os.environ:
        os.environ["NP_LOCAL_PORT"] = os.environ["EXEC_LOCAL_PORT"]

    NP_LOCAL_PORT = os.getenv("NP_LOCAL_PORT") \
        or input("local port you want to be converted:")

    for _ in range(3):
        NP_REMOTE_PORT = os.getenv("NP_REMOTE_PORT") \
            or input(f"remote port you want to convert `{NP_LOCAL_PORT}` to:")
        if NP_REMOTE_PORT and NP_REMOTE_PORT != NP_LOCAL_PORT:
            break

    tunnel_addr = f"{os.environ['NP_SERVER_ADDRESS']}:{os.getenv('NP_SERVER_PORT', '10101')}"
    target_addr = f":{NP_LOCAL_PORT}"

    app = nodepass(); app.run([f"client://{tunnel_addr}/{target_addr}"], app.download(tagVer=os.getenv("NP_VERSION", "latest")))