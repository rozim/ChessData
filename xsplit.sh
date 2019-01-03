#!/bin/bash -e

for d in $1; do
    echo $d
    for f in $d/*.pgn; do
	echo $f
	python Code/xsplit.py ${f}
    done
done
