#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, platform, urllib.request, subprocess


HTTPGET = urllib.request.urlopen


class frpc:

    RELEASES_URL = os.environ.get("GHPROXY","") + \
        "https://github.com/fatedier/frp/releases"

    DEFAULT_ARCH = dict({
        "i386": "386", 
        "x86_64": "amd64", 
        "armv6l": "arm", "armv7l": "arm", 
        "armv8l": "arm64", "aarch64": "arm64", 
    }).get(platform.machine().lower(), platform.machine().lower())

    TARGET = dict({
        "windows": "frp_{tagVer}_windows_{arch}.zip",
        "linux": "frp_{tagVer}_linux_{arch}.tar.gz",
        "darwin": "frp_{tagVer}_darwin_{arch}.tar.gz",
    })[platform.system().lower()]


    def latest(self):
        resp = HTTPGET( "/".join([self.RELEASES_URL, "latest"]) )
        tagVer = str(resp.url).split("tag/")[-1]
        return tagVer

    def download(self, tagVer="latest"):
        if tagVer == "latest": tagVer = self.latest()
        downUrl = "/".join([
            self.RELEASES_URL, "download", tagVer,
            self.TARGET.format(tagVer=tagVer[1:], arch=self.DEFAULT_ARCH)])
        resp = HTTPGET(downUrl)
        if (200 == resp.status):
            return self.extract(
                resp.read(), 
                target=os.path.basename(downUrl), tagVer=tagVer)
        raise Exception("download failed: " + downUrl)

    def extract(self, data, target='', tagVer=''):
        import io, tarfile, zipfile
        if target.endswith("tar.gz"):
            tarfile.open(fileobj=io.BytesIO(data)).extractall()
        elif target.endswith("zip"):
            zipfile.ZipFile(io.BytesIO(data)).extractall()
        return list(filter(lambda x: x.startswith(f"frp_{tagVer[1:]}") and os.path.isdir(x), os.listdir()))[0]

    def run(self, argv=[], pathdir="."):
        app = os.path.join(pathdir, "frpc")
        self.app = subprocess.Popen([app]+argv)



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