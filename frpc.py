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
                if system.arch in asset and system.system in asset]

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

    if "frpc_token" not in os.environ \
    or "frpc_server_addr" not in os.environ \
    or "frpc_local_port" not in os.environ \
    or "frpc_remote_port" not in os.environ:
        print("warn: frpc_token, frpc_server_addr, frpc_local_port, frpc_remote_port must be set\n")
        exit(1)

    cmd = [
        os.environ.get("frpc_protocol", "tcp"),
        "--remote_port", os.environ['frpc_remote_port'],
        "--local_port", os.environ['frpc_local_port'],
        "--server_addr", os.environ['frpc_server_addr'].strip('\"'),
        "--token", os.environ['frpc_token'].strip('\"')]

    if "frpc_user" in os.environ:
        cmd += ["--user", os.environ['frpc_user']]

    app = frpc(); app.run(cmd, app.download())
    if (app.app and "frpc_wait" in os.environ): app.app.wait()