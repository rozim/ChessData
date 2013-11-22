

for fn in `ls *.pgn | grep -v fix-`
do
    fix="fix-${fn}"
    if [ ! -f ${fix} ]; then
        echo $fix
        python fix.py $fn
    fi
done