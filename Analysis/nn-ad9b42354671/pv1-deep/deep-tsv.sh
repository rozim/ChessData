# python ../../../Code/analysis-db-to-tsv.py deep.sqlite > deep.tsv



for fn in twic-btm-150-26.sqlite twic-btm-25-25.sqlite twic-wtm-150-26.sqlite twic-wtm-25-25.sqlite; do
    bn=$(basename $fn .sqlite)
    python ../../../Code/analysis-db-to-tsv.py ${fn} > ${bn}.tsv
done
