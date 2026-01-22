#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, io, sys, re, time, types, platform, urllib.request, subprocess, zipfile, tarfile, lzma


HTTPGET = urllib.request.urlopen
NOHTTPGET = urllib.request.build_opener(
    urllib.request.ProxyHandler({})).open

IS_64BIT = bool(sys.maxsize > 2**32)
IS_ARM64 = os.path.exists(os.path.expandvars("$SystemRoot\\System32\\xtajit64.dll"))


class EXTRACT:
    @staticmethod
    def extract(data, target_dir=None, target_name=None):
        if data[0:4] == b"\x50\x4b\x03\x04":
            return EXTRACT.zip(data, target_dir)
        if data[0:4] == b"\x1f\x8b\x08\x00":
            return EXTRACT.tar(data, target_dir)
        if data[0:4] == b"\xFD\x37\x7A\x58":
            return EXTRACT.xz(data, target_dir, target_name)
        else:
            return EXTRACT.bin(data, target_dir, target_name)

    @staticmethod
    def zip(data, target_dir=None, zipfilter=None):
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            if archive.infolist()[0].filename.endswith("/") and \
                not target_dir:
                target_dir = archive.infolist()[0].filename
            for member in filter(zipfilter, archive.infolist()):
                archive.extract(member, target_dir)
        return os.path.abspath(os.path.join(os.getcwd(), target_dir or ''))

    @staticmethod
    def tar(data, target_dir):
        tarfile.open(fileobj=io.BytesIO(data)).extractall(target_dir)
        return os.path.join(os.getcwd(), target_dir)

    @staticmethod
    def bin(data, target_dir='', target_name=''):
        target = os.path.join(target_dir, target_name or 'unknown_file')
        os.makedirs(target_dir, exist_ok=True)
        with open(target, "wb") as fp:
            fp.write(data)
        return os.path.join(os.getcwd(), target)

    @staticmethod
    def xz(data, target_dir='', target_name=''):
        if not target_name:
            target_name = "extracted_file"
        if target_name.endswith(".xz"):
            target_name = target_name[:-3]
        return EXTRACT.bin(lzma.decompress(data), target_dir, target_name)


class GITHUB_RELEASES:
    def __init__(self, source=None, author=None, project=None):
        if (None == source) and (None == author or None == project):
            raise Exception("author and project must be specified")
        self.RELEASES_URL = f"https://github.com/{author}/{project}/releases" \
            if None == source else f"https://github.com/{str(source).split('/')[0]}/{str(source).split('/')[1]}/releases"
    def latest(self):
        resp = HTTPGET( "/".join([self.RELEASES_URL, "latest"]) )
        tagVer = str(resp.url).split("tag/")[-1]
        return tagVer
    def assets(self, tagVer):
        if "latest" == tagVer: tagVer = self.latest()
        resp = HTTPGET( "/".join([self.RELEASES_URL, "expanded_assets", tagVer]) )
        return re.findall("<a href=\"(.*?)\"", resp.read().decode())
    def geturl(self, re_pattern=".zip", tagVer="latest"):
        target = list(filter(lambda href: re.search(re_pattern, href), self.assets(tagVer)))[0]
        return f"https://github.com/{target}"


@staticmethod
def download2(url, timeout=60, retries=3, chunk_size=1024*1024):
    last_error = None
    
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            resp = urllib.request.urlopen(req, timeout=timeout)
            
            content_length = resp.headers.get('Content-Length')
            total_size = int(content_length) if content_length else 0
            
            data = io.BytesIO()
            downloaded = 0
            
            while True:
                chunk = resp.read(chunk_size)
                if not chunk:
                    break
                data.write(chunk)
                downloaded += len(chunk)
                
                # 可选：显示进度
                if total_size:
                    progress = downloaded * 100 // total_size
                    print(f"\r【{url.split('/')[-1]}】Downloading: {downloaded // (1024*1024)}MB / {total_size // (1024*1024)}MB ({progress}%)", end='', flush=True)
            
            if total_size:
                print()  # 换行
            
            return data.getvalue()
            
        except Exception as e:
            last_error = e
            print(f"\nDownload attempt {attempt + 1}/{retries} failed: {e}")
            if attempt < retries - 1:
                wait_time = 2 ** attempt  # 指数退避: 1s, 2s, 4s
                print(f"Retrying in {wait_time}s...")
                time.sleep(wait_time)
    
    raise Exception(f"Download failed after {retries} attempts: {last_error}")


# if not bool(os.environ.get("DEBUGPY_RUNNING")):
#     target = "utils/common"
#     RAW_CODE = HTTPGET(f"https://github.com/nblog/cloud-py3-example/blob/main/{target}.py?raw=true").read().decode('utf-8')

#     utils_module = types.ModuleType('utils')
#     sys.modules['utils'] = utils_module

#     raw_module = types.ModuleType('common')
#     sys.modules['utils.common'] = raw_module
#     setattr(utils_module, 'common', raw_module)

#     exec(RAW_CODE, raw_module.__dict__)