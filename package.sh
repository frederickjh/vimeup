#!/bin/bash -e
# Load configuration
source package_config.sh

# Set the Python program to make executables from and the basename of the executable.
python_program=vimeup.py
executable_name=vimeup

    FULL_PY_PATH=$(readlink -f $python_program)
    SOURCE_DIR_LINUX=$(dirname ${FULL_PY_PATH})
    MAIN_PY=$(basename ${FULL_PY_PATH})
    PROJECT_NAME="$executable_name"

function loadcolor(){
# Colors  http://wiki.bash-hackers.org/snipplets/add_color_to_your_scripts
# More info about colors in bash http://misc.flogisoft.com/bash/tip_colors_and_formatting
esc_seq="\x1b["  #In Bash, the <Esc> character can be obtained with the following syntaxes:  \e  \033  \x1B
NC=$esc_seq"39;49;00m" # NC = Normal Color
# Colors with black background (40;)set for emails.
red=$esc_seq"31;40;01m"
green=$esc_seq"32;40;00m"
yellow=$esc_seq"33;40;01m"
blue=$esc_seq"34;40;01m"
magenta=$esc_seq"35;40;01m"
cyan=$esc_seq"36;40;01m"
}
loadcolor

echo -e "${yellow}>> ${green}Now building the ${cyan}Windows${green} executable for ${blue}$PROJECT_NAME${green}.${NC}"
echo ""

THIS_SCRIPT_PATH=`readlink -f $0`
THIS_SCRIPT_DIR=`dirname ${THIS_SCRIPT_PATH}`




WINE_TARBALL=${THIS_SCRIPT_DIR}/build_environment/wine.tar.gz

if [ ! -e "${WINE_TARBALL}" ]; then
    echo "ERROR: You don't have a frozen wine environment at"
    echo "${WINE_TARBALL}"
    echo
    echo "Option 1:"
    echo "    Create a new wine environment by running build_environment/create.sh"
    echo "    and following the instructions."
    echo "Option 2:"
    echo "    Use an existing wine environment (with Python installed) by doing:"
    echo "    $ export WINEPREFIX=~/.wine    # path to your existing wine env"
    echo "    $ build_environment/freeze.sh"

    exit 2
else
    export WINEPREFIX=`mktemp -d --suffix=_wine`

    # Unpack wine environment
    tar "--directory=${WINEPREFIX}" -xzf ${WINE_TARBALL}

fi

BUILD_DIR_LINUX=${WINEPREFIX}/drive_c/win-build
BUILD_DIR_WIN="C:\\win-build"
mkdir -p ${BUILD_DIR_LINUX}

# Create symbolic link to source directory so Windows can access it
ln -s ${SOURCE_DIR_LINUX} ${BUILD_DIR_LINUX}/src_symlink
SOURCE_DIR_WIN=${BUILD_DIR_WIN}\\src_symlink

# PIP FETCH
echo builddir is ${BUILD_DIR_LINUX}
if [ -x "$(command -v wget)" ]; then
  wget https://bootstrap.pypa.io/get-pip.py -O ${BUILD_DIR_LINUX}/get-pip.py
elif [ -x "$(command -v curl)" ]; then
  curl https://bootstrap.pypa.io/get-pip.py >${BUILD_DIR_LINUX}/get-pip.py
else
  echo "couldn't find a way to retrieve get-pip.py from the web"
  exit 1
fi # PIP FETCH

wine "${PYTHON_EXE_WIN}" "${BUILD_DIR_WIN}\\get-pip.py"

wine "${PYTHON_EXE_WIN}" "-m" "pip" "install" "pyinstaller"

if [ -f ${SOURCE_DIR_LINUX}/requirements.txt ]; then
    wine "${PYTHON_EXE_WIN}" "-m" "pip" "install" "-r" \
        "${SOURCE_DIR_WIN}\\requirements.txt"
fi # [ -f requirements.txt ]

# NOTE - if using hooks, your spec'file should have a line like:
# hookspath=["C:\\build\\src_symlink\\hooks\\"],

echo -e -n "#\n# RUNNING PYINSTALLER\n#\n"

wine "${PYTHON_EXE_WIN}" "-m" "PyInstaller" \
    "--name=${PROJECT_NAME}" \
    --onedir \
    --noconsole \
    --noconfirm \
    --icon=logo/vimeup.ico \
    --add-data "privatespec.ini;." \
    --add-data "localspec.ini;." \
    --add-data "locale;locale" \
    --add-data "logo/vimeup.ico;logo" \
    --add-data "logo/vimeup.png;logo" \
    --distpath "win-dist" \
    --workpath "win-build" \
    "${SOURCE_DIR_WIN}\\${MAIN_PY}"

rm -rf ${WINEPREFIX}
mkdir -p win-dist/${PROJECT_NAME}/vimeo-configuration

echo ""
echo -e "${yellow}>> ${green}The ${cyan}Windows${green} executable available at ${blue}win-dist/${PROJECT_NAME}/${PROJECT_NAME}.exe${green}.${NC}"
echo ""


echo -e "${yellow}>> ${green}Now building the ${cyan}Linux${green} executable for ${blue}$PROJECT_NAME${green}.${NC}"
echo ""

pyinstaller --onedir \
            --noconsole \
            --noconfirm \
            --icon=logo/vimeup.png \
            --add-data "privatespec.ini:." \
            --add-data "localspec.ini:." \
            --add-data "locale:locale" \
            --add-data "logo/vimeup.png:logo" \
            --distpath "lin-dist" \
            --workpath "lin-build" \
            vimeup.py
mkdir -p lin-dist/${PROJECT_NAME}/vimeo-configuration

echo ""
echo -e "${yellow}>> ${green}The ${cyan}Linux${green} executable available at ${blue}lin-dist/${PROJECT_NAME}/${PROJECT_NAME}${green}.${NC}"
echo ""