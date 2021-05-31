# Packaging Vimeup and creating a Windows Installer

## Python Packager
Original project [gregretkowski/python-windows-packager](https://github.com/gregretkowski/python-windows-packager) has been abandoned. I did a fork of it and a quick update to Python 3, [ frederickjh/python-windows-packager](https://github.com/frederickjh/python-windows-packager).
### Overview

Develop Python on Linux, deploy on Windows.

Uses Pyinstaller and Wine to "freeze" Python programs to a standalone Windows
executable, all from your Linux box.

### Quick start

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

### Modifying the Python Windows environment

If you want to use a different Python version or add additional Python
modules, just do the above with different Windows Python installers.

## Inno Setup

[Inno Setup](https://jrsoftware.org/isinfo.php) can be used with wine on Linux to create a Windows' Installer. *Inno Setup* is a know application in Play on Linux and can be used to create an installer for Vimeup using its *Inno Setup Script* file `vimeup.iss` that is saved in the repository.

NOTE: `git` will replace CRLF in vimeup.iss by LF. The file will have its original line endings in the working directory. Whether this will be an issue when running *Inno Setup* or if the LF line endings will need to be converted back to CRLF first 