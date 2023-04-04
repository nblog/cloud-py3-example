
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
cd /d %USERPROFILE%\Downloads

set NOCURL=0
set DOWNLOADURL=https://repo.huaweicloud.com/python/3.8.10/python-3.8.10-amd64.exe
set PYTHON3=%ProgramFiles%\Python38
set PYINSTALLCFG=InstallAllUsers=1 PrependPath=1
if 0 equ %NOCURL% (curl %DOWNLOADURL% -o pysetup.exe) else (certutil -urlcache -split -f %DOWNLOADURL% pysetup.exe)
pysetup.exe /quiet %PYINSTALLCFG%
set PATH=%PYTHON3%\;%PYTHON3%\Scripts\;%PATH%
```