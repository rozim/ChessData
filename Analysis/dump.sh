

for fn in *.sqlite; do
    if [ $fn == mega.sqlite ] ; then
	echo MEGA
    else
	sql=$(basename $fn .sqlite).sql
	echo $fn :: $sql
	echo " "
	sqlite3 ${fn} <<EOF
.output ${sql}
.dump
.quit
EOF
    fi
done
