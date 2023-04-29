
### usage
```
win cmd >
set RUNPY=has-root.py
set DOWNURL=https://github.com/nblog/cloud-py3-example/blob/main/%RUNPY%?raw=true
set NOSSL=import ssl;ssl._create_default_https_context=ssl._create_unverified_context;
python -c "%NOSSL%import urllib.request;HTTPGET=urllib.request.urlopen;exec(HTTPGET('%DOWNURL%').read().decode('utf-8'))"
```

```
linux shell >
export RUNPY=has-root.py
export DOWNURL=https://github.com/nblog/cloud-py3-example/blob/main/${RUNPY}?raw=true
export NOSSL="import ssl;ssl._create_default_https_context=ssl._create_unverified_context;"
python3 -c "${NOSSL}import urllib.request;HTTPGET=urllib.request.urlopen;exec(HTTPGET('${DOWNURL}').read().decode('utf-8'))"
```

### quick python (windows)
```
cmd >
cd /d %USERPROFILE%\Downloads

set NOCURL=0
set DOWNLOADURL=http://repo.huaweicloud.com/python/3.8.10/python-3.8.10-amd64.exe
set PYTHON3=%SystemDrive%\Python\Python38
set PYINSTALLCFG=InstallAllUsers=1 PrependPath=1 Include_test=0 TargetDir=%PYTHON3%
if 0 equ %NOCURL% (curl %DOWNLOADURL% -o pysetup.exe) else (certutil -urlcache -split -f %DOWNLOADURL% pysetup.exe)
pysetup.exe /quiet %PYINSTALLCFG%
set PATH=%PYTHON3%\;%PYTHON3%\Scripts\;%PATH%
```