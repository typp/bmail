# !/bin/bash

PYTHON_PKGS=(PyYAML)

virtualenv -p /usr/bin/python3.3 $PWD/venv
source $PWD/venv/bin/activate

cp -r libs/{PyQt4,sip.so} venv/lib/python3.3/site-packages/

for pkg in ${PYTHON_PKGS[*]}
do
     pip install $pkg
done
