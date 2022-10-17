# python ../../../Code/analysis-db-to-tsv.py deep.sqlite > deep.tsv



for fn in twic-v2-btm-150-26.sqlite twic-v2-btm-25-25.sqlite twic-v2-wtm-150-26.sqlite twic-v2-wtm-25-25.sqlite; do
    bn=$(basename $fn .sqlite)
    python ../../../Code/analysis-db-to-tsv.py ${fn} > ${bn}.tsv
done
