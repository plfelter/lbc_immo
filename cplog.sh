#!/bin/bash

source_dir="/home/lobstr/writeable/."
dest_dir="/home/debian/lbc_immo/data/lobstr_delivery"
log_file="/home/debian/lbc_immo/data/cplog.log"

function copy_and_log {
        cp_result=$(cp -rnv $source_dir $dest_dir)
        if [ ! -z "$cp_result" ]; then
                echo >> $log_file
                date | tee -a $log_file
                echo "$cp_result" | tee -a $log_file
        fi
}

while :
do
        copy_and_log
        sleep 2
done
