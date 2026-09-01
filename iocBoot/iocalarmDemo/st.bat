REM So previous PATH can be restored.
set OLD_PATH=%PATH%
REM Path to this file.
set BatchDir=%~dp0
pushd %BatchDir%
pushd ..\..\
set TOP=%CD%
REM https://superuser.com/questions/428088/find-a-directory-folder-with-cmd-without-knowing-full-path
dir /b %TOP%\python3* > %TEMP%\py_build_ver.txt
set /p py_build_ver= < %TEMP%\py_build_ver.txt
REM See https://ss64.com/nt/syntax-replace.html
set "py3_ver=%py_build_ver:python3=%"
py -3.%py3_ver% -c "import os, sys; print(os.path.dirname(sys.executable))" > %TEMP%\py_path.txt
set /p py_path= < %TEMP%\py_path.txt
set PATH=C:\Windows\system32;%py_path%
popd
call dllPath.bat
@echo on
..\..\bin\windows-x64\alarmDemo.exe st.cmd
popd
@echo off
set PATH=%OLD_PATH%
