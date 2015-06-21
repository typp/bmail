# !/bin/bash

PYTHON_PKGS=(PyYAML)

virtualenv -p /usr/bin/python3 $PWD/venv
source $PWD/venv/bin/activate

cp -r /usr/lib/python3.4/site-packages/{PyQt5,sip.so} venv/lib/python3.4/site-packages/

for pkg in ${PYTHON_PKGS[*]}
do
     pip install --disable-pip-version-check --isolated --no-cache-dir $pkg
done
