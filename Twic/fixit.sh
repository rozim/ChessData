set -e
for fn in `ls twic*.pgn | grep -v fix-`
do
    fix="fix-${fn}"
    python3 fix.py ${fn}
    if cmp -s ${fn} ${fix}; then
	echo " "
	rm -f ${fix}
    else
	echo DIFF ${fn}
	mv ${fix} ${fn}
    fi
done
