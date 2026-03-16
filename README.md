
### usage (uvx)

```bash
# run any script directly
uvx --from git+https://github.com/nblog/cloud-py3-example frida-server
uvx --from git+https://github.com/nblog/cloud-py3-example x64dbg

# wan2local orchestrator
uvx --from git+https://github.com/nblog/cloud-py3-example wan2local --local frida-server --wan frpc

# list available scripts
uvx --from git+https://github.com/nblog/cloud-py3-example wan2local --list
```

### available scripts

| Script | Description |
|---|---|
| `frida-server` | Download & run frida-server |
| `frpc` | Download & run frpc tunnel |
| `nodepass` | Download & run nodepass tunnel |
| `x64dbg` | Download x64dbg + plugins + tools |
| `dnspyex` | Download dnSpyEx + ILSpy |
| `ghidra` | Download Ghidra + OpenJDK |
| `llvm-mingw` | Download LLVM MinGW toolchain |
| `has-root` | Check administrator/root privileges |
| `dynamic-pip` | Bootstrap pip + install packages |
| `driver-test` | WDK driver test setup |
| `vs-runtime` | Install .NET Framework + VC Runtime |
| `vs-remote` | Install VS Remote Debugger |
| `vnc-server` | Install TightVNC server |
| `ms-rdp` | RDP Wrapper setup |
| `win7sp1` | Windows 7 SP1 patches (stub) |
| `wan2local` | Orchestrate local service + WAN tunnel |

### legacy usage

<details>
<summary>python -c (no uv required)</summary>

**win cmd >**
```
set "RUNPY=has-root"
set "DOWNURL=https://github.com/nblog/cloud-py3-example/raw/main/%RUNPY%.py"
set "NOSSL=import ssl;ssl._create_default_https_context=ssl._create_unverified_context;"
python -c "%NOSSL%import urllib.request;HTTPGET=urllib.request.urlopen;exec(HTTPGET('%DOWNURL%').read().decode('utf-8'))"
```

**unix bash >**
```
export "RUNPY=has-root"
export "DOWNURL=https://github.com/nblog/cloud-py3-example/raw/main/${RUNPY}.py"
export "NOSSL=import ssl;ssl._create_default_https_context=ssl._create_unverified_context;"
python3 -c "${NOSSL}import urllib.request;HTTPGET=urllib.request.urlopen;exec(HTTPGET('${DOWNURL}').read().decode('utf-8'))"
```

</details>

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
