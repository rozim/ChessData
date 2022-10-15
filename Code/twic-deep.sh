

# twic-btm-150-26.txt
# twic-wtm-150-26.txt

ind=../Release/2022-10-05/
outd=../Analysis/nn-ad9b42354671/pv1-deep
depth=20
python -u fen-analysis-db.py --fen=${ind}/twic-wtm-25-25.txt --output=${outd}/twic-wtm-25-25.sqlite --depth=${depth} > ${outd}/twic-wtm-25-25.txt 2>&1 &
python -u fen-analysis-db.py --fen=${ind}/twic-btm-25-25.txt --output=${outd}/twic-btm-25-25.sqlite --depth=${depth} > ${outd}/twic-btm-25-25.txt 2>&1 &

python -u fen-analysis-db.py --fen=${ind}/twic-wtm-150-26.txt --output=${outd}/twic-wtm-150-26.sqlite --depth=${depth} > ${outd}/twic-wtm-150-26.txt 2>&1 &
python -u fen-analysis-db.py --fen=${ind}/twic-btm-150-26.txt --output=${outd}/twic-btm-150-26.sqlite --depth=${depth} > ${outd}/twic-btm-150-26.txt 2>&1
wait
wait
wait


# --reference=../Analysis/nn-ad9b42354671/pv1-deep/deep.sqlite
