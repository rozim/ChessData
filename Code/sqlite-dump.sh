
if [ $# -eq 1 ]
then
    files=$1
else
    files=*.sqlite
fi


for fn in ${files}; do
    sql=$(basename $fn .sqlite).sql
    echo $fn :: $sql
    echo " "
    sqlite3 ${fn} <<EOF
.output ${sql}
.dump
.quit
EOF

done
