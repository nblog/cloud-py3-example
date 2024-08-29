#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, re, platform, urllib.request, subprocess


HTTPGET = urllib.request.urlopen


class frpc:

    RELEASES_URL = "https://github.com/fatedier/frp/releases"

    class TARGET:
        arch = dict({
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
        try:
            if target.endswith("tar.gz"):
                tarfile.open(fileobj=io.BytesIO(data)).extractall()
            elif target.endswith("zip"):
                zipfile.ZipFile(io.BytesIO(data)).extractall()
        except PermissionError:
            pass # may be running

        target = [f for f in os.listdir() if f.startswith( \
            re.findall("frp_[0-9.]+_", target)[0])][0]
        return os.path.join(os.getcwd(), target)

    def run(self, argv=[], target_dir="."):
        binpath = os.path.join(target_dir, "frpc")
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

    FRPC_LOCAL_PORT = os.environ.get("FRPC_LOCAL_PORT") \
        or input("local port you want to be converted:")

    FRPC_REMOTE_PORT = os.environ.get("FRPC_REMOTE_PORT") \
        or input(f"remote port you want to convert `{FRPC_LOCAL_PORT}` to:")

    cmd = [
        os.environ.get("FRPC_PROTOCOL", "tcp"),
        "--proxy_name", os.environ.get("FRPC_PROXY_NAME", socket.gethostname()),
        "--local_port", FRPC_LOCAL_PORT, "--remote_port", FRPC_REMOTE_PORT,
        "--server_port", os.environ["FRPC_SERVER_PORT"],
        "--server_addr", os.environ["FRPC_SERVER_ADDRESS"],
        "--token", os.environ["FRPC_TOKEN"]]

    if "FRPC_USER" in os.environ:
        cmd += ["--user", os.environ["FRPC_USER"]]

    app = frpc(); app.run(cmd, app.download())