
### usage
```
cmd >
SET GHPROXY=https://ghproxy.com/
SET DOWNURL=%GHPROXY%https://github.com/nblog/cloud-py3-example/blob/main/has-root.py?raw=true
python -c "import urllib.request;HTTPGET=urllib.request.urlopen;exec(HTTPGET('%DOWNURL%').read().decode('utf-8'))"
```

### quick python (windows)
```
cmd >
SET DOWNLOADURL=https://repo.huaweicloud.com/python/3.8.10/python-3.8.10-amd64.exe
certutil -urlcache -split -f %DOWNLOADURL% && python-3.8.10-amd64.exe /quiet && SET "PYTHON38=%LOCALAPPDATA%\Programs\Python\Python38"
SET PATH=%PYTHON38%\;%PYTHON38%\Scripts\;%PATH%
```