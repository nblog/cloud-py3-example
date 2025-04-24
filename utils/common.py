#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, io, sys, re, types, platform, urllib.request, subprocess, zipfile, tarfile, lzma


HTTPGET = urllib.request.urlopen
NOHTTPGET = urllib.request.build_opener(
    urllib.request.ProxyHandler({})).open

IS_64BIT = bool(sys.maxsize > 2**32)
IS_ARM64 = os.path.exists(os.path.expandvars("$SystemRoot\\System32\\xtajit64.dll"))


class EXTRACT:

    @staticmethod
    def zip(data, target_dir, zipfilter=None):
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            if archive.infolist()[0].filename.endswith("/"):
                target_dir = archive.infolist()[0].filename
            for member in filter(zipfilter, archive.infolist()):
                archive.extract(member, target_dir)
        return os.path.abspath(os.path.join(os.getcwd(), target_dir))

    @staticmethod
    def tar(data, target_dir):
        tarfile.open(fileobj=io.BytesIO(data)).extractall(target_dir)
        return os.path.join(os.getcwd(), target_dir)

    @staticmethod
    def bin(data, target_dir, target_name):
        target = os.path.join(target_dir, target_name)
        os.makedirs(target_dir, exist_ok=True)
        with open(target, "wb") as fp:
            fp.write(data)
        return os.path.join(os.getcwd(), target)

    @staticmethod
    def xz(data, target_dir, target_name=''):
        if target_name.endswith(".xz"):
            target_name = target_name[:-3]
        return EXTRACT.bin(lzma.decompress(data), target_dir, target_name)


class GITHUB_RELEASES:
    def __init__(self, source=None, author=None, project=None):
        if (None == source) and (None == author or None == project):
            raise Exception("author and project must be specified")
        self.RELEASES_URL = f"https://github.com/{author}/{project}/releases" \
            if None == source else f"https://github.com/{str.split(source, '/')[0]}/{str.split(source, '/')[1]}/releases"
    def latest(self):
        resp = HTTPGET( "/".join([self.RELEASES_URL, "latest"]) )
        tagVer = str(resp.url).split("tag/")[-1]
        return tagVer
    def assets(self, tagVer):
        if "latest" == tagVer: tagVer = self.latest()
        resp = HTTPGET( "/".join([self.RELEASES_URL, "expanded_assets", tagVer]) )
        return re.findall("<a href=\"(.*?)\"", resp.read().decode())
    def geturl(self, re_pattern="\.zip", tagVer="latest"):
        target = list(filter(lambda href: re.search(re_pattern, href), self.assets(tagVer)))[0]
        return f"https://github.com/{target}"


# if not bool(os.environ.get("DEBUGPY_RUNNING")):
#     target = "utils/common"
#     RAW_CODE = HTTPGET(f"https://github.com/nblog/cloud-py3-example/blob/main/{target}.py?raw=true").read().decode('utf-8')

#     utils_module = types.ModuleType('utils')
#     sys.modules['utils'] = utils_module

#     raw_module = types.ModuleType('common')
#     sys.modules['utils.common'] = raw_module
#     setattr(utils_module, 'common', raw_module)

#     exec(RAW_CODE, raw_module.__dict__)