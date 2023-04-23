#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, re, platform, urllib.request, subprocess


HTTPGET = urllib.request.urlopen



class WDKTEST:

    HOST_TARGET = "http://192.168.56.1:8080"

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
            WORK_DIR = os.path.expandvars("%SYSTEMDRIVE%\\KDNET")
            os.makedirs(WORK_DIR, exist_ok=True)

            for _ in ["kdnet.exe", "VerifiedNICList.xml"]:
                resp = HTTPGET('/'.join([
                    WDKTEST.HOST_TARGET,
                    "Debuggers", "x64", _]))

                with open(os.path.join(WORK_DIR, os.path.basename(resp.url)), "wb") as f:
                    f.write(resp.read())

    class TEST:

        @staticmethod
        def tool():
            ''' https://learn.microsoft.com/windows-hardware/drivers/gettingstarted/provision-a-target-computer-wdk-8-1 '''
            WORK_DIR = os.path.expandvars("%SYSTEMDRIVE%\\drivertest")
            os.makedirs(WORK_DIR, exist_ok=True)
            
            resp = HTTPGET('/'.join([
                WDKTEST.HOST_TARGET, 
                "Remote", "x64", "WDK%20Test%20Target%20Setup%20x64-x64_en-us.msi"]))

            with open(os.path.join(WORK_DIR, os.path.basename(resp.url)), "wb") as f:
                f.write(resp.read())

            subprocess.check_call([
                "msiexec", "/i", os.path.join(WORK_DIR, os.path.basename(resp.url)),
                "/qn"], cwd=WORK_DIR, shell=True)


# python -m http.server 8080 --directory "%ProgramFiles(x86)%\Windows Kits\10"
WDKTEST.TEST.tool(), WDKTEST.KDNET.kdnet(), exit(0)


raise NotImplementedError("driver test is not implemented yet")


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

