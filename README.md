
### usage (uvx)

```bash
# run any script directly
uvx --from git+https://github.com/nblog/cloud-py3-example x64dbg

# wan2local orchestrator
uvx --from git+https://github.com/nblog/cloud-py3-example wan2local --local frida-server
```

### available scripts

| Script | Description |
|---|---|
| `has-root` | Check administrator/root privileges |
| `x64dbg` | Download x64dbg + plugins + tools |
| `ghidra` | Download Ghidra + OpenJDK |
| `wan2local` | Orchestrate local service + WAN tunnel |

### quick python ([windows](https://docs.python.org/3/using/windows.html#installing-without-ui))
```
:: install python3.12
if exist "%SystemRoot%\SyChpe32" (set "TARGET_ARCH=arm64") else (set "TARGET_ARCH=amd64")
set "DOWNLOADURL=http://repo.huaweicloud.com/python/3.12.10/python-3.12.10-%TARGET_ARCH%.exe"
set "PYTHON3=%SystemDrive%\Python\Python312"
set "PYINSTALLCFG=InstallAllUsers=1 PrependPath=1 Include_test=0 TargetDir=%PYTHON3%"
set "OUTPUTNAME=pysetup.exe"
pushd %USERPROFILE%\Downloads
curl --version >NUL 2>&1
if %ERRORLEVEL% EQU 0 (set USECURL=1) else (set USECURL=0)
if %USECURL% NEQ 0 (curl -fsSL %DOWNLOADURL% -o %OUTPUTNAME%) else (certutil -urlcache -split -f %DOWNLOADURL% %OUTPUTNAME%)
call %OUTPUTNAME% /passive %PYINSTALLCFG%
popd
set "PATH=%PYTHON3%\;%PYTHON3%\Scripts\;%PATH%"
pushd %PYTHON3% && mklink python3.exe python.exe && popd
```
