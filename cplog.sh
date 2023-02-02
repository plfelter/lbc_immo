log_file="log.txt"
source_dir="./cptest"
dest_dir="./cptest4"

function copy_and_log {
        cp_result=$(cp -rnv $source_dir $dest_dir)
        if [ ! -z "$cp_result" ]; then
                echo "$cp_result"
                echo >> $log_file
                date >> $log_file
                echo "$cp_result" >> $log_file
        fi
}

while :
do
        copy_and_log
        sleep 2
done
