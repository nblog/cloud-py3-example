#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, re, platform, urllib.request, subprocess


HTTPGET = urllib.request.urlopen


class EXTRACT:

    @staticmethod
    def zip(data, target_dir):
        import io, zipfile
        zipfile.ZipFile(io.BytesIO(data)).extractall(target_dir)
        return os.path.join(os.getcwd(), target_dir)

    @staticmethod
    def tar(data, target_dir):
        import io, tarfile
        tarfile.open(fileobj=io.BytesIO(data)).extractall(target_dir)
        return os.path.join(os.getcwd(), target_dir)



class dnSpyEx:

    RELEASES_URL = "https://github.com/dnSpyEx/dnSpy/releases"


    def latest(self):
        resp = HTTPGET( "/".join([self.RELEASES_URL, "latest"]) )
        tagVer = str(resp.url).split("tag/")[-1]
        return tagVer

    def assets(self, tagVer):
        resp = HTTPGET( "/".join([self.RELEASES_URL, "expanded_assets", tagVer]) )
        assets = re.findall(">(dnSpy-net-.*?.zip)<", resp.read().decode())
        return assets

    def download(self, tagVer="latest", target_dir='dnSpy'):
        if tagVer == "latest": tagVer = self.latest()

        succeed = ''
        for target in self.assets(tagVer):
            downUrl = "/".join([self.RELEASES_URL, "download", tagVer, target])
            resp = HTTPGET(downUrl)
            if (200 == resp.status):
                succeed = EXTRACT.zip(resp.read(), target_dir=os.path.join( \
                    target_dir, os.path.splitext(os.path.basename(downUrl))[0]))

                if (not succeed):
                    raise Exception("download failed: " + downUrl)

        return succeed


if __name__ == "__main__":

    dnSpyEx().download()