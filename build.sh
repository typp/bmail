#!/bin/bash

PYTHON_PKGS=(PyYAML)

virtualenv -p /usr/bin/python2.7 $PWD/venv
source $PWD/venv/bin/activate

for pkg in ${PYTHON_PKGS[*]}
do
     pip install --disable-pip-version-check --isolated --no-cache-dir $pkg
done

