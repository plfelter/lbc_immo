#!/bin/bash

script_dir=$(dirname -- "$( readlink -f -- "$0"; )";)
cd $script_dir
python3 main.py
