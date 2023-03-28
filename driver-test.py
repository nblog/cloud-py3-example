#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, platform, urllib.request, subprocess


HTTPGET = urllib.request.urlopen


raise NotImplementedError("driver test is not implemented yet")



os.environ.setdefault("PIP_INSTALL_PACKAGES", "pywin32")
DOWNURL = os.environ.get("GHPROXY","") + \
f"https://github.com/nblog/cloud-py3-example/blob/main/dynamic-pip.py?raw=true"
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



class WDKTEST:

    # raise NotImplementedError("WDKTEST is not implemented yet")

    class KDNET:

        ''' https://learn.microsoft.com/windows-hardware/drivers/debugger/setting-up-a-network-debugging-connection '''
        os.makedirs(os.path.join(os.environ.get("SYSTEMDRIVE", "C:"), "KDNET"), exist_ok=True)

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

    class TEST:

        @staticmethod
        def tool():
            '''  '''
