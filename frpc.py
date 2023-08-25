#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, re, platform, urllib.request, subprocess


HTTPGET = urllib.request.urlopen


class frpc:

    RELEASES_URL = "https://github.com/fatedier/frp/releases"

    class TARGET:
        arch = dict({
            "i386": "386", 
            "x86_64": "amd64", 
            "armv6l": "arm", "armv7l": "arm", 
            "armv8l": "arm64", "aarch64": "arm64", 
        }).get(platform.machine().lower(), platform.machine().lower())

        system = platform.system().lower()


    def latest(self):
        resp = HTTPGET( "/".join([self.RELEASES_URL, "latest"]) )
        tagVer = str(resp.url).split("tag/")[-1]
        return tagVer

    def assets(self, tagVer, system=TARGET):
        resp = HTTPGET( "/".join([self.RELEASES_URL, "expanded_assets", tagVer]) )
        assets = re.findall(">(frp_.*?)<", resp.read().decode())
        return [asset for asset in assets \
                if system.system in asset and system.arch in asset]

    def download(self, tagVer="latest"):
        if tagVer == "latest": tagVer = self.latest()
        target = self.assets(tagVer)[0]
        downUrl = "/".join([self.RELEASES_URL, "download", tagVer, target])
        resp = HTTPGET(downUrl)
        if (200 == resp.status):
            return self.extract(resp.read(), target)
        raise Exception("download failed: " + downUrl)

    def extract(self, data, target=''):
        import io, zipfile, tarfile
        if target.endswith("tar.gz"):
            tarfile.open(fileobj=io.BytesIO(data)).extractall()
        elif target.endswith("zip"):
            zipfile.ZipFile(io.BytesIO(data)).extractall()

        target = [f for f in os.listdir() if f.startswith(target[:9])][0]
        return os.path.join(os.getcwd(), target)

    def run(self, argv=[], target_dir="."):
        binpath = os.path.join(target_dir, "frpc")
        self.app = subprocess.Popen([binpath]+argv)



if __name__ == "__main__":

    if "FRPC_SERVER_ADDRESS" not in os.environ \
        or "FRPC_TOKEN" not in os.environ:
        print("error: `FRPC_SERVER_ADDRESS` `FRPC_TOKEN` must be set\n"); exit(1)

    if ("FRPC_REMOTE_PORT" in os.environ):
        FRPC_REMOTE_PORT = os.environ["FRPC_REMOTE_PORT"]
    else: FRPC_REMOTE_PORT = input("remote port you want to convert to:")

    if ("FRPC_LOCAL_PORT" in os.environ):
        FRPC_LOCAL_PORT = os.environ["FRPC_LOCAL_PORT"]
    else: FRPC_LOCAL_PORT = input("local port you want to be converted:")

    cmd = [
        os.environ.get("FRPC_PROTOCOL", "tcp"),
        "--local_port", FRPC_LOCAL_PORT, "--remote_port", FRPC_REMOTE_PORT,
        "--server_addr", os.environ["FRPC_SERVER_ADDRESS"].strip('\"'),
        "--token", os.environ["FRPC_TOKEN"].strip('\"')]

    if "FRPC_USER" in os.environ:
        cmd += ["--user", os.environ["FRPC_USER"]]

    app = frpc(); app.run(cmd, app.download())