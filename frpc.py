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


class frpc:
    ''' https://github.com/fatedier/frp/releases '''

    class TARGET:
        system = platform.system().lower()
        arch = dict({
            "x86_64": "amd64", 
            "armv6l": "arm", "armv7l": "arm", 
            "armv8l": "arm64", "aarch64": "arm64", 
        }).get(platform.machine().lower(), platform.machine().lower())

    def download(self, target_dir="frp", tagVer="latest"):
        downUrl = GITHUB_RELEASES(source="fatedier/frp").geturl(f"frp_.*?_{frpc.TARGET.system}_{frpc.TARGET.arch}.*?", tagVer)
        resp = HTTPGET(downUrl)
        if (200 == resp.status):
            return self.extract(resp.read(), target_dir='.', target_name=os.path.basename(downUrl))
        raise Exception("download failed: " + downUrl)

    def extract(self, data, target_dir, target_name=''):
        try:
            EXTRACT.extract(data, target_dir=target_dir, target_name=target_name)
        except PermissionError:
            pass # may be running
        target = next(f for f in os.listdir(target_dir) if f.startswith(re.findall(r"frp_[0-9.]+_", target_name)[0]))
        return os.path.join(os.getcwd(), target_dir, target)

    def run(self, argv=[], target_dir="."):
        binpath = os.path.abspath(os.path.join(target_dir, "frpc"))
        self.app = subprocess.Popen([binpath]+argv)



if __name__ == "__main__":

    import socket

    if "FRPC_TOKEN" not in os.environ \
        or "FRPC_SERVER_ADDRESS" not in os.environ \
        or "FRPC_SERVER_PORT" not in os.environ:
        print("error:",
            " `FRPC_TOKEN`"
            " `FRPC_SERVER_ADDRESS`"
            " `FRPC_SERVER_PORT`"
            " must be set\n"); exit(1)

    if "EXEC_LOCAL_PORT" in os.environ:
        os.environ["FRPC_LOCAL_PORT"] = os.environ["EXEC_LOCAL_PORT"]

    FRPC_LOCAL_PORT = os.environ.get("FRPC_LOCAL_PORT") \
        or input("local port you want to be converted:")

    for _ in range(3):
        FRPC_REMOTE_PORT = os.environ.get("FRPC_REMOTE_PORT") \
            or input(f"remote port you want to convert `{FRPC_LOCAL_PORT}` to:")
        if FRPC_REMOTE_PORT and FRPC_REMOTE_PORT != FRPC_LOCAL_PORT:
            break

    cmd = [
        os.environ.get("FRPC_PROTOCOL", "tcp"),
        "--proxy_name", os.environ.get("FRPC_PROXY_NAME", socket.gethostname()),
        "--local_port", FRPC_LOCAL_PORT, "--remote_port", FRPC_REMOTE_PORT,
        "--server_port", os.environ["FRPC_SERVER_PORT"],
        "--server_addr", os.environ["FRPC_SERVER_ADDRESS"],
        "--token", os.environ["FRPC_TOKEN"]]

    if "FRPC_USER" in os.environ:
        cmd += ["--user", os.environ["FRPC_USER"]]

    # 'v0.54.0' was the last one to support windows7
    app = frpc()
    for _ in range(3):
        try:
            app.run(cmd, app.download(tagVer=os.environ.get("FRPC_VERSION", "latest")))
            break
        except (FileNotFoundError, OSError):
            input("⚠  " "frpc binary not executable, retrying...")