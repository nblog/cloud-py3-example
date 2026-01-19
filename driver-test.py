#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, io, sys, re, types, platform, subprocess, urllib.request

HTTPGET = urllib.request.urlopen

if not bool(os.environ.get("DEBUGPY_RUNNING")):
    source = "utils/common"
    RAW_CODE = HTTPGET(f"https://github.com/nblog/cloud-py3-example/blob/main/{source}.py?raw=true").read().decode('utf-8')

    raw_module = types.ModuleType(source.split('/')[-1])
    sys.modules[source.replace('/', '.')] = raw_module
    exec(RAW_CODE, raw_module.__dict__)

from utils.common import (
    NOHTTPGET, EXTRACT, IS_64BIT, IS_ARM64
)


class subprocess:
    @staticmethod
    def getoutput(cmd):
        @staticmethod
        def _decode_output(data: bytes) -> str:
            if not data:
                return ''
            encodings = ['utf-8', 'utf-8-sig', 'gbk', 'cp936', 'latin-1']
            for enc in encodings:
                try:
                    return data.decode(enc)
                except (UnicodeDecodeError, LookupError):
                    continue
            return data.decode('utf-8', errors='replace')

        import subprocess
        try:
            result = subprocess.run(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                shell=True
            )
            return _decode_output(result.stdout)
        except Exception:
            import subprocess as sp
            return sp.getoutput(cmd)


class WDKTEST:

    KITROOT = os.path.join(os.path.expandvars("%ProgramFiles(x86)%"), "Windows Kits", "10")

    TARGET_HOST = ['192.168.56.1', 8080]

    TARGET_ARCH = IS_ARM64 and 'ARM64' or \
            (IS_64BIT and 'x64' or 'x86')

    @staticmethod
    def network_host_name():
        import socket; return socket.gethostname()

    @staticmethod
    def network_host_name2():
        target = WDKTEST.network_host_name()
        from urllib.error import HTTPError
        try:
            NOHTTPGET('/'.join([
                f"http://{WDKTEST.TARGET_HOST[0]}:{WDKTEST.TARGET_HOST[1]}", 
                ":Target", target]))
        except HTTPError as e:
            if e.code != 404: raise e
        return target


    class TEST:
        @staticmethod
        def tools():
            ''' https://learn.microsoft.com/windows-hardware/drivers/gettingstarted/provision-a-target-computer-wdk-8-1 '''
            WORK_DIR = os.path.expandvars(os.path.join("$SystemDrive", "DriverTest"))
            os.makedirs(WORK_DIR, exist_ok=True)

            from urllib.parse import quote
            target = f"WDK Test Target Setup {WDKTEST.TARGET_ARCH}-{WDKTEST.TARGET_ARCH.lower()}_en-us.msi"

            resp = NOHTTPGET('/'.join([
                f"http://{WDKTEST.TARGET_HOST[0]}:{WDKTEST.TARGET_HOST[1]}", 
                "Remote", WDKTEST.TARGET_ARCH, quote(target)]))

            import subprocess
            subprocess.check_call([
                "msiexec", "/i", EXTRACT.bin(resp.read(), WORK_DIR, target),
                "/qn"], cwd=WORK_DIR, shell=True)

            ''' check '''
            "netstat -an | FINDSTR \"50005\""

        @staticmethod
        def usbview():
            # https://github.com/microsoft/Windows-driver-samples/tree/main/usb/usbview
            # https://learn.microsoft.com/windows-hardware/drivers/debugger/setting-up-a-usb-3-0-debug-cable-connection#set-up-the-target-computer
            WORK_DIR = os.path.expandvars(os.path.join("$SYSTEMDRIVE", "DriverTest", "usbview"))
            os.makedirs(WORK_DIR, exist_ok=True)

            for _ in ["usbview.exe", "usbview.exe.config"]:
                resp = NOHTTPGET('/'.join([
                    f"http://{WDKTEST.TARGET_HOST[0]}:{WDKTEST.TARGET_HOST[1]}", 
                    "Debuggers", WDKTEST.TARGET_ARCH.lower(), _]))
                EXTRACT.bin(resp.read(), WORK_DIR, _)

    class KDNET:
        @staticmethod
        def kdnet():
            # https://learn.microsoft.com/windows-hardware/drivers/debugger/setting-up-a-network-debugging-connection#set-up-the-target-computer
            # https://learn.microsoft.com/windows-hardware/drivers/debugger/setting-up-a-network-debugging-connection-automatically#enable-other-debugging-types
            WORK_DIR = os.path.expandvars(os.path.join("$SYSTEMDRIVE", "KDNET"))
            os.makedirs(WORK_DIR, exist_ok=True)

            for _ in ["kdnet.exe", "VerifiedNICList.xml"]:
                resp = NOHTTPGET('/'.join([
                    f"http://{WDKTEST.TARGET_HOST[0]}:{WDKTEST.TARGET_HOST[1]}", 
                    "Debuggers", WDKTEST.TARGET_ARCH.lower(), _]))
                EXTRACT.bin(resp.read(), WORK_DIR, _)

        @staticmethod
        def freeport():
            import socket
            for port in range(50000,50040):
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.bind(('' , port))
                    s.close()
                    return port
                except: pass
            raise Exception("no free port")


class NETWORK:
    class connProfile:
        name: str; category: str
        def __init__(self, name: str, category: str):
            self.name = name; self.category = category

    class interfaceCfg:
        index: int; alias: str; address: str; subnet: str
        @staticmethod
        def address(output):
            output = re.findall(r"IP.*?:\s+([\d\.]+)[\n\r]", output)
            return output[0] if (output) else ''
        @staticmethod
        def subnet(output):
            output = re.findall(r":\s+([\d\.]+\.0)\/\d+ \(.*? ([\d\.]+)\)[\n\r]", output)
            return output[0] if (output) else ''
        def __init__(self, index: int, alias: str):
            self.index = index; self.alias = alias
            output = subprocess.getoutput(f"netsh interface ipv4 show addresses name={self.index}")
            self.address = self.address(output)
            self.subnet = self.subnet(output)

    def __init__(self):
        output = re.findall( \
            "([0-9]+): (.*?)[\n\r]", 
            subprocess.getoutput("netsh interface ipv4 show ipaddresses"))

        self.ethernet = \
            list(filter( \
                lambda e: e.address and e.address != '127.0.0.1', 
                map(lambda e: NETWORK.interfaceCfg(e[0], e[1]), output)))

        output = re.findall(
            r"(Name|Category)\s+:\s+(.*?)[\n\r]",
            NETWORK.psex("Get-NetConnectionProfile"))
        self.network = [ \
            NETWORK.connProfile(output[_][1], output[_ + 1][1]) \
                for _ in range(0, len(output), 2)]

    def reference(self):
        print("\nreference:")
        for i, e in enumerate(self.ethernet):
            print(f"{i + 1}. {e.address} / {e.subnet[0]} / {e.alias}")
        print()

        # f"netsh interface ipv4 set address name={e.index} static {e.address} {e.subnet[1]} {WDKTEST.TARGET_HOST[0]}"


    @staticmethod
    def psex(pscommand):
        extend = ''
        if (platform.uname().release == '7'):
            ''' https://gist.github.com/ITMicaH/65cd447d1ba10ed9accc '''
            ps1 = os.path.join(os.getcwd(), "NetConnectionProfiles.ps1")
            extend = f"Import-Module \'{ps1}\'; "
        return subprocess.getoutput( \
            f"powershell -ExecutionPolicy Bypass -Command \"{extend + pscommand}\"")

    def network_category(self, NetworkCategory='Private'):
        print("\nnetwork:")

        for i, e in enumerate(self.network):
            print(f"{i + 1}. {e.name} ({e.category})")
        print()

        i = int(input(f"switch network to {NetworkCategory.lower()}:").lower()[0])
        if (i < 1 or i > len(self.network)): return

        NETWORK.psex(f"Set-NetConnectionProfile -Name \'{self.network[i-1].name}\' -NetworkCategory {NetworkCategory}")



''' runas `administrator` '''
os.environ.setdefault("HAS_ROOT", "1")
DOWNURL = f"https://github.com/nblog/cloud-py3-example/blob/main/has-root.py?raw=true"
exec(HTTPGET(DOWNURL).read().decode('utf-8'))

''' check `Windows Secure Boot` '''
import winreg
try:
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\SecureBoot\State") as key:
        if (winreg.QueryValueEx(key, "UEFISecureBootEnabled")[0]):
            print("\n\n"
                + "⚠️ WARNING:\n"
                + "Windows Secure Boot is ENABLED.\n"
                + "You will NOT be able to load self-signed drivers.\n"
                + "Please disable Secure Boot in BIOS/UEFI settings to proceed.\n\n")
except FileNotFoundError: pass

''' check `Microsoft Vulnerable Driver Blocklist` '''
try:
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\CI\Config") as key:
        blocklist_enabled = winreg.QueryValueEx(key, "VulnerableDriverBlocklistEnable")[0]
        if blocklist_enabled:
            print("\n\n"
                + "⚠️ WARNING:\n"
                + "Microsoft vulnerable driver blocklist is ENABLED.\n"
                + "Drivers signed with revoked certificates may fail to load (STATUS_IMAGE_CERT_REVOKED / 0xC0000603).\n"
                + "To allow these drivers, set 'VulnerableDriverBlocklistEnable' to 0 and reboot:\n"
                + "HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\CI\\Config\n\n")
except FileNotFoundError: pass
except OSError: pass

# ------------------------------------------------

''' reference target host '''
NETWORK().reference(); print()


for _ in range(3):
    host_input = input("Please enter the host address: ").strip()
    if not host_input:
        continue
    WDKTEST.TARGET_HOST[0] = host_input
    break
else:
    print(f"Using default host: {WDKTEST.TARGET_HOST[0]}")


cmd = \
f'''

python -m http.server --directory \"{WDKTEST.KITROOT}\" {WDKTEST.TARGET_HOST[1]} 

'''
print("\n\n"
    + "⚠️ IMPORTANT:\n" \
    + "Before entering the following command, please ensure\n" \
    + "that the host computer has installed the same version of the\n" \
    + f"`Windows Driver Kit (WDK)` as the current computer system version ({platform.version()}):\n\n" \
    + "Download WDK: https://learn.microsoft.com/windows-hardware/drivers/download-the-wdk#download-icon-for-wdk-step-3-install-the-wdk\n\n" \
    + (" && ".join([cmd.strip()]))
); input()
WDKTEST.TEST.tools(); WDKTEST.KDNET.usbview(); WDKTEST.KDNET.kdnet()

# https://learn.microsoft.com/windows-hardware/drivers/devtest/bcdedit--bootdebug#comments
# bcdedit /bootdebug {bootmgr} on
if input("enable bootmgr debug (y/[n]):").lower().startswith("y"):
    print(subprocess.getoutput("bcdedit /bootdebug {bootmgr} on"))
# bcdedit /bootdebug {default} on
if input("enable winload debug (y/[n]]):").lower().startswith("y"):
    print(subprocess.getoutput("bcdedit /bootdebug on"))
# bcdedit /debug {default} on
# if input("enable kernel debug (y/[n]):").lower().startswith("y"):
#     print(subprocess.getoutput("bcdedit /debug on"))


if (input("install debugger toolchain (y/[n]):").lower().startswith("y")):
    batch = [
        # ("https://download.sysinternals.com/files/Sysmon.zip", EXTRACT.zip, "sysmon"),
        # ("https://www.osronline.com/OsrDown.cfm/osrloaderv30.zip", EXTRACT.zip, "OsrLoader"),
        ("https://download.sysinternals.com/files/DebugView.zip", EXTRACT.zip, "debugview"),
        ("https://github.com/GTHF/trash_package/raw/main/KmdManager.exe", EXTRACT.bin, "kmdmanager.exe"),
    ]
    for i in batch:
        resp = HTTPGET(i[0])
        if (200 == resp.status):
            target_dir = os.path.expandvars( \
                os.path.join("$PUBLIC", "Desktop", "debugger-toolchain"))
            if (EXTRACT.bin == i[1]):
                print(f'setup: {i[1](resp.read(), target_dir=target_dir, target_name=i[2])}')
            if (EXTRACT.zip == i[1]):
                target_dir = os.path.join(target_dir, i[2])
                print(f'setup: {i[1](resp.read(), target_dir=target_dir)}')


print(f"\nDone! configure `Extensions->Driver->Test->Configure Devices` in Visual Studio.\n")
print("--------------------------------")
print(f"\n`Network Host Name`: `{WDKTEST.network_host_name2()}`\n")

input(); exit(0)


raise NotImplementedError("driver test is not implemented yet")



''' https://github.com/vivisect/vivsys/tree/master/vivsys '''

try:
    from win32.lib import win32serviceutil
except ImportError:
    os.environ.setdefault("PIP_INSTALL_PACKAGES", "pywin32")
    DOWNURL = f"https://github.com/nblog/cloud-py3-example/blob/main/dynamic-pip.py?raw=true"
    exec(HTTPGET(DOWNURL).read().decode('utf-8'))


from win32 import win32service
from win32.lib import win32serviceutil


class kmdmanager:
    def __init__(self, driver_file, service_name='', symlink=''):
        self.driver_file = driver_file
        if (not service_name): 
            self.service_name = os.path.splitext(os.path.basename(driver_file))[0]
        if (not symlink):
            self.symlink = "\\\\.\\" + self.service_name

    def reg2run(self):
        return self.register() and self.run()
    def stop2unreg(self):
        return self.stop() and self.unregister()

    def unregister(self):
        try:
            win32serviceutil.RemoveService(self.service_name)
            return bool(1)
        except: return False
    def register(self):
        try:
            win32serviceutil.InstallService(
                None, self.service_name,
                os.path.splitext(os.path.basename(self.driver_file))[0])
            return bool(1)
        except Exception as e:
            ''' 1073: The specified service already exists '''
            return bool(1073 == e.winerror)

    def stop(self):
        try:
            win32serviceutil.StopService(self.service_name) and \
            win32serviceutil.WaitForServiceStatus(
                self.service_name, win32service.SERVICE_STOPPED)
            return True
        except Exception as e:
            print(f"failed to stop service {e.winerror}: {e.strerror}")
            return False
    def run(self):
        try:
            win32serviceutil.StartService(self.service_name) and \
            win32serviceutil.WaitForServiceStatus(
                self.service_name, win32service.SERVICE_RUNNING)
            return True
        except Exception as e:
            print(f"failed to start service {e.winerror}: {e.strerror}")
            return False

    def ioctl(self, ioctl, inbuf=b'', outbuf_size=0):
        import win32file
        try:
            handle = win32file.CreateFile(self.symlink,
                win32file.GENERIC_READ | win32file.GENERIC_WRITE, 
                0, None, win32file.OPEN_EXISTING, 
                0, None
            )
            outbuf = win32file.AllocateReadBuffer(outbuf_size)
            win32file.DeviceIoControl(
                handle, ioctl, inbuf, outbuf, None
            )
            win32file.CloseHandle(handle)
            return bytearray(outbuf)
        except Exception as e:
            print(f"failed to ioctl {e.winerror}: {e.strerror}")
            return bytearray()

