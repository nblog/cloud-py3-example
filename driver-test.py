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
    TARGET_HOST = 'http://192.168.56.1:8080'

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
                WDKTEST.TARGET_HOST, 
                "Remote", WDKTEST.TARGET_ARCH, quote(target)]))

            with open(os.path.join(WORK_DIR, target), "wb") as f:
                f.write(resp.read())

            subprocess.check_call([
                "msiexec", "/i", os.path.join(WORK_DIR, target),
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
                    WDKTEST.TARGET_HOST,
                    "Debuggers", "x64", _]))

                with open(os.path.join(WORK_DIR, os.path.basename(resp.url)), "wb") as f:
                    f.write(resp.read())

    class NETWORK:
        ''' https://gist.github.com/ITMicaH/65cd447d1ba10ed9accc '''
        ''' https://learn.microsoft.com/windows/win32/api/netlistmgr/nn-netlistmgr-inetworklistmanager '''

        class ConnProfile:
            name: str; alias: str; index: int; ip: str
            def __init__(self, name: str, alias: str, index: int):
                self.name = name; self.alias = alias; 
                self.index = index; self.ip = self.get_ip()
            def get_ip(self):
                import locale
                output = re.findall( \
                    "IPAddress\s+:\s(.*?)\s\s", subprocess.check_output( \
                        "powershell -command "
                        + f"\"Get-NetIPAddress -InterfaceIndex {self.index} -AddressFamily IPv4\"", shell=True) \
                            .decode(locale.getpreferredencoding()))
                return output[0] if output else ''

        def __init__(self):
            import locale
            output = re.findall( \
                "Name\s+:\s(.*?)\s\s"
                "InterfaceAlias\s+:\s(.*?)\s\s"
                "InterfaceIndex\s+:\s(.*?)\s\s",
                subprocess.check_output( \
                    "powershell -command "
                    + "\"Get-NetConnectionProfile\"", shell=True) \
                        .decode(locale.getpreferredencoding()))

            self.ethernet = [WDKTEST.NETWORK.ConnProfile(e[0], e[1], e[2]) for e in output]

        def network(self, NetworkCategory='Private'):
            print("\nreference:")
            for i, e in enumerate(self.ethernet):
                print(f"{i + 1}. {e.alias} ({e.name}) / {e.ip}")
            print(); i = int(input(f"switch to {NetworkCategory.lower()} network:").lower()[0])
            if (i < 1 or i > len(self.ethernet)): return
            ps = f"\"Get-NetConnectionProfile -InterfaceIndex {self.ethernet[i-1].index} | Set-NetConnectionProfile -NetworkCategory {NetworkCategory}\""
            subprocess.call("powershell -command " + ps, shell=True)



''' runas `administrator` '''
os.environ.setdefault("HAS_ROOT", "1")
DOWNURL = f"https://github.com/nblog/cloud-py3-example/blob/main/has-root.py?raw=true"
exec(HTTPGET(DOWNURL).read().decode('utf-8'))



''' reference target host '''
WDKTEST.NETWORK().network(); print()


'''  '''
WDKTEST.TARGET_HOST = \
    f'http://{input("please enter the Host IP address: ").strip()}:8080'

cmd = \
r'''

python -m http.server 8080 --directory "%ProgramFiles(x86)%\Windows Kits\10"

'''
print(
    "\nmake sure that the host has the `WDK` installed" + 
    "before entering the following command:\n\n" + cmd.strip()
); os.system("pause")
WDKTEST.TEST.tools(); WDKTEST.KDNET.kdnet()

if (input("install debugger toolchain (y/n):").lower()[0] == 'y'):
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

