@echo off

SET PYTHON3=%SystemDrive%\Python\Python38

SET PYINSTALLCFG=InstallAllUsers=1 PrependPath=1 Include_test=0 TargetDir=%PYTHON3%


SET DOWNLOADURL=http://repo.huaweicloud.com/python/3.8.10/python-3.8.10-amd64.exe
SET OUTPUTNAME=pysetup.exe

PUSHD %USERPROFILE%\Downloads

curl --version >NUL 2>&1
IF %ERRORLEVEL% EQU 0 (SET USECURL=1) ELSE (SET USECURL=0)

IF %USECURL% NEQ 0 (curl %DOWNLOADURL% -o %OUTPUTNAME%) ELSE (certutil -urlcache -f -split %DOWNLOADURL% %OUTPUTNAME%)

CALL %OUTPUTNAME% /quiet %PYINSTALLCFG%

POPD


SET PATH=%PYTHON3%\;%PYTHON3%\Scripts\;%PATH%