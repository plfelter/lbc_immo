#!/bin/bash

source $(poetry --directory=/home/debian/lbc_immo env info --path)/bin/activate
python /home/debian/lbc_immo/lbc_immo/main.py
deactivate
