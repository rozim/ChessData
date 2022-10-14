
for fn in $*; do
    sqlite3 ${fn} <<EOF
.dump
.quit
EOF

done
