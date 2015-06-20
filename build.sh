#!/bin/bash

PYTHON_PKGS=(requirements.txt)

INSTALL_PATH=$PWD/.libs
LINK_PATH=$PWD/libs

mkdir -p .libs

for pkg in ${PYTHON_PKGS[*]}
do
    pip install  --disable-pip-version-check --isolated --no-use-wheel --no-cache-dir --install-option="--prefix=$INSTALL_PATH" -r $pkg 
done

ln -fs $INSTALL_PATH/lib/python3.4/site-packages/ $LINK_PATH
