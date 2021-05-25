# Python Packager
## Overview

Develop Python on Linux, deploy on Windows.

Uses Pyinstaller and Wine to "freeze" Python programs to a standalone Windows
executable, all from your Linux box.

## Quick start

To quickly build your Wine environment, then create a standalone EXE,
run the following commands:

```bash
mkdir installers
cd installers
wget "https://www.python.org/ftp/python/3.6.8/python-3.6.8.exe" 
wget "https://github.com/mhammond/pywin32/releases/download/b300/pywin32-300.win32-py3.6.exe"
cd ..
build_environment/create.sh
export WINEPREFIX=/tmp/path-outputted-from-create
wine start installers/python-3.6.8.exe
```
In the Python installer
* Tick **Add Python *[version number]* to PATH**
* Select **Customize installation** > **Next**  > **Customize install location** > 
   * C:\Python
```bash
wine start installers/pywin32-300.win32-py3.6.exe
build_environment/freeze.sh
./package.sh sample-application/src/main.py MySampleProgram
```

This will create a Wine environment in a tarball at 
./build_environment/wine.tar.gz.

## Modifying the Python Windows environment

If you want to use a different Python version or add additional Python
modules, just do the above with different Windows Python installers.

## Known Issues
* sample-application does not work with Python 3, pull requests welcome.