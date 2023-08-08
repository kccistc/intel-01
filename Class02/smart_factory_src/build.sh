#!/bin/bash

pip3 uninstall iotdemo-0.0.1-py2.py3-none-any.whl
python3 setup.py bdist_wheel --universal
pip3 install --force-reinstall dist/iotdemo-0.0.1-py2.py3-none-any.whl
