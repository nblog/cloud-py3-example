#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, re, platform, urllib.request, subprocess


HTTPGET = urllib.request.urlopen
NOHTTPGET = urllib.request.build_opener(
    urllib.request.ProxyHandler({})).open


class EXTRACT:

    @staticmethod
    def zip(data, target_dir, zipfilter=None):
        import io, zipfile
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            for member in filter(zipfilter, archive.infolist()):
                archive.extract(member, target_dir)
        return os.path.join(os.getcwd(), target_dir)

    @staticmethod
    def tar(data, target_dir):
        import io, tarfile
        tarfile.open(fileobj=io.BytesIO(data)).extractall(target_dir)
        return os.path.join(os.getcwd(), target_dir)

    @staticmethod
    def bin(data, target_dir, target_name):
        target = os.path.join(target_dir, target_name)
        os.makedirs(target_dir, exist_ok=True)
        open(target, "wb").write(data)
        return target


class WDKTEST:

    ''' default: vbox '''
    TARGET_HOST = ['192.168.56.1', 8080]

    ''' default: x64 '''
    TARGET_ARCH = 'x64'

    @staticmethod
    def network_host_name():
        import socket; return socket.gethostname()

    class TEST:

        @staticmethod
        def tools():
            ''' https://learn.microsoft.com/windows-hardware/drivers/gettingstarted/provision-a-target-computer-wdk-8-1 '''
            WORK_DIR = os.path.expandvars(os.path.join("$SYSTEMDRIVE", "drivertest"))
            os.makedirs(WORK_DIR, exist_ok=True)

            from urllib.parse import quote
            target = f"WDK Test Target Setup {WDKTEST.TARGET_ARCH}-{WDKTEST.TARGET_ARCH}_en-us.msi"

            resp = NOHTTPGET('/'.join([
                f"http://{WDKTEST.TARGET_HOST[0]}:{str(WDKTEST.TARGET_HOST[1])}", 
                "Remote", WDKTEST.TARGET_ARCH, quote(target)]))

            subprocess.check_call([
                "msiexec", "/i", EXTRACT.bin(resp.read(), WORK_DIR, target),
                "/qn"], cwd=WORK_DIR, shell=True)

    class KDNET:

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

        @staticmethod
        def kdnet():
            ''' https://learn.microsoft.com/windows-hardware/drivers/debugger/setting-up-a-network-debugging-connection '''
            WORK_DIR = os.path.expandvars(os.path.join("$SYSTEMDRIVE", "KDNET"))
            os.makedirs(WORK_DIR, exist_ok=True)

            for _ in ["kdnet.exe", "VerifiedNICList.xml"]:
                resp = NOHTTPGET('/'.join([
                    f"http://{WDKTEST.TARGET_HOST[0]}:{str(WDKTEST.TARGET_HOST[1])}", 
                    "Debuggers", "x64", _]))

                EXTRACT.bin(resp.read(), WORK_DIR, os.path.basename(resp.url))


class NETWORK:
    class connProfile:
        name: str; category: str
        def __init__(self, name: str, category: str):
            self.name = name; self.category = category

    class interfaceCfg:
        index: int; name: str; address: str; subnet: str
        def __init__(self, index: int, name: str):
            self.index = index; self.name = name
            self.address = self.get_ipv4()
            self.subnet = self.get_subnet()
        def get_ipv4(self):
            output = re.findall( \
                "IP.*?:\s+([\d\.]+)[\n\r]",
                subprocess.getoutput(f"netsh interface ipv4 show addresses name={self.index}"))
            return output[0] if (output) else ''
        def get_subnet(self):
            output = re.findall( \
                ":\s+([\d\.]+\.0)\/\d+ \(.*? ([\d\.]+)\)[\n\r]",
                subprocess.getoutput(f"netsh interface ipv4 show addresses name={self.index}"))
            return output[0] if (output) else ''

    def __init__(self):
        output = re.findall( \
            "([0-9]+): (.*?)[\n\r]", 
            subprocess.getoutput("netsh interface ipv4 show ipaddresses"))
        self.ethernet = \
            list(filter( \
                lambda e: e.address, 
                map(lambda e: NETWORK.interfaceCfg(e[0], e[1]), output)))

        output = re.findall( \
            "(Name|Category)\s+:\s+(.*?)[\n\r]", 
            NETWORK.psex("Get-NetConnectionProfile"))
        self.network = [ \
            NETWORK.connProfile(output[_][1], output[_ + 1][1]) \
                for _ in range(0, len(output), 2)]

    def reference(self):
        print("\nreference:")
        for i, e in enumerate(self.ethernet):
            print(f"{i + 1}. {e.address} ({e.name})")
        print()

        f"netsh interface ipv4 set address name={e.index} static {e.address} {e.subnet[1]} {WDKTEST.TARGET_HOST[0]}"


    @staticmethod
    def psex(pscommand):
        extend = ''
        if (platform.platform().startswith("Windows-7")):
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

        i = int(input(f"switch to {NetworkCategory.lower()} network:").lower()[0])
        if (i < 1 or i > len(self.network)): return

        NETWORK.psex(f"Set-NetConnectionProfile -Name \'{self.network[i-1].name}\' -NetworkCategory {NetworkCategory}")



''' runas `administrator` '''
os.environ.setdefault("HAS_ROOT", "1")
DOWNURL = f"https://github.com/nblog/cloud-py3-example/blob/main/has-root.py?raw=true"
exec(HTTPGET(DOWNURL).read().decode('utf-8'))



''' reference target host '''
NETWORK().reference(); print()


WDKTEST.TARGET_HOST[0] = \
    input("please enter the Host IP address: ").strip()


cmd = \
f'''

python -m http.server 8080 --directory "%ProgramFiles(x86)%\Windows Kits\10"

'''
print(
    "\nmake sure that the host has the `WDK` installed" + 
    "before entering the following command:\n\n" + cmd.strip()
); os.system("pause")
WDKTEST.TEST.tools(); WDKTEST.KDNET.kdnet()

if (input("install debugger toolchain (y/n):").lower().startswith("y")):
    batch = [
        ("https://download.sysinternals.com/files/DebugView.zip", EXTRACT.zip, "debugview"),
    ]
    for i in batch:
        resp = HTTPGET(i[0])
        if (200 == resp.status):
            target_dir = os.path.expandvars( \
                os.path.join("$USERPROFILE", "Desktop", "sysinternals", i[2]))

            print(f'setup: {i[1](resp.read(), target_dir=target_dir)}')


print("Done! configure `Extensions->Driver->Test->Configure Devices` in Visual Studio.\n")
print("--------------------------------")
print("`Network Host Name`: `" + WDKTEST.network_host_name() + "`\n")

os.system("pause"); exit(0)


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

