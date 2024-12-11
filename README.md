
### usage

**win cmd >**
```
set "RUNPY=has-root"
set "DOWNURL=https://github.com/nblog/cloud-py3-example/blob/main/%RUNPY%.py?raw=true"
set "NOSSL=import ssl;ssl._create_default_https_context=ssl._create_unverified_context;"
python -c "%NOSSL%import urllib.request;HTTPGET=urllib.request.urlopen;exec(HTTPGET('%DOWNURL%').read().decode('utf-8'))"
```

**unix bash >**
```
export "RUNPY=has-root"
export "DOWNURL=https://github.com/nblog/cloud-py3-example/blob/main/${RUNPY}.py?raw=true"
export "NOSSL=import ssl;ssl._create_default_https_context=ssl._create_unverified_context;"
python3 -c "${NOSSL}import urllib.request;HTTPGET=urllib.request.urlopen;exec(HTTPGET('${DOWNURL}').read().decode('utf-8'))"
```

### quick python ([windows](https://docs.python.org/3/using/windows.html#installing-without-ui))
```
:: install python3.11.9
if exist "%SystemRoot%\System32\xtajit64.dll" (set "TARGET_ARCH=arm64") else (set "TARGET_ARCH=amd64")
set "DOWNLOADURL=http://repo.huaweicloud.com/python/3.11.9/python-3.11.9-%TARGET_ARCH%.exe"
set "PYTHON3=%SystemDrive%\Python\Python311"
set "PYINSTALLCFG=InstallAllUsers=1 PrependPath=1 Include_test=0 TargetDir=%PYTHON3%"
set "OUTPUTNAME=pysetup.exe"
pushd %USERPROFILE%\Downloads
curl --version >NUL 2>&1
if %ERRORLEVEL% EQU 0 (set USECURL=1) else (set USECURL=0)
if %USECURL% NEQ 0 (curl -fsSL %DOWNLOADURL% -o %OUTPUTNAME%) else (certutil -urlcache -split -f %DOWNLOADURL% %OUTPUTNAME%)
call %OUTPUTNAME% /passive %PYINSTALLCFG%
popd
set "PATH=%PYTHON3%\;%PYTHON3%\Scripts\;%PATH%"
```