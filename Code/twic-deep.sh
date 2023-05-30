#!/bin/bash

ind=../Release/2022-10-05/
outd=../Analysis/nn-ad9b42354671/pv1-deep

for depth in {32..32}; do
    echo DEPTH: $depth
    python -u fen-analysis-db.py --fen=${ind}/twic-v2-wtm-25-25.txt  --output=${outd}/twic-v2-wtm-25-25.sqlite  --depth=${depth} > ${outd}/twic-v2-wtm-25-25-${depth}.txt 2>&1 &
    python -u fen-analysis-db.py --fen=${ind}/twic-v2-btm-25-25.txt  --output=${outd}/twic-v2-btm-25-25.sqlite  --depth=${depth} > ${outd}/twic-v2-btm-25-25-${depth}.txt 2>&1 &
    python -u fen-analysis-db.py --fen=${ind}/twic-v2-wtm-150-26.txt --output=${outd}/twic-v2-wtm-150-26.sqlite --depth=${depth} > ${outd}/twic-v2-wtm-150-26-${depth}.txt 2>&1 &
    python -u fen-analysis-db.py --fen=${ind}/twic-v2-btm-150-26.txt --output=${outd}/twic-v2-btm-150-26.sqlite --depth=${depth} > ${outd}/twic-v2-btm-150-26-${depth}.txt 2>&1

    wait
    wait
    wait
done
