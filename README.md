
### usage
```
win cmd >
set GHPROXY=https://ghproxy.com/
set DOWNURL=%GHPROXY%https://github.com/nblog/cloud-py3-example/blob/main/has-root.py?raw=true
set NOSSL=import ssl;ssl._create_default_https_context=ssl._create_unverified_context;
python -c "%NOSSL%import urllib.request;HTTPGET=urllib.request.urlopen;exec(HTTPGET('%DOWNURL%').read().decode('utf-8'))"
```

```
linux shell >
export GHPROXY=https://ghproxy.com/
export DOWNURL=${GHPROXY}https://github.com/nblog/cloud-py3-example/blob/main/has-root.py?raw=true
python3 -c "import urllib.request;HTTPGET=urllib.request.urlopen;exec(HTTPGET('$DOWNURL').read().decode('utf-8'))"
```

### quick python (windows)
```
cmd >
set DOWNLOADURL=https://repo.huaweicloud.com/python/3.8.10/python-3.8.10-amd64.exe
certutil -urlcache -split -f %DOWNLOADURL% && python-3.8.10-amd64.exe /quiet && set "PYTHON38=%LOCALAPPDATA%\Programs\Python\Python38"
set PATH=%PYTHON38%\;%PYTHON38%\Scripts\;%PATH%
```