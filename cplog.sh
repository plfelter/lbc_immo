log_file="log.txt"
cp_result=$(cp -rnv ./cptest ./cptest4)
if [ ! -z "$cp_result" ]; then
        echo "$cp_result"
        echo >> $log_file
        date >> $log_file
        echo "$cp_result" >> $log_file
fi
