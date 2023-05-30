set -e

for shard in 0 1 2 3 4 5 6 7 8 9
do
    echo $shard
    python -u fen-analysis-db.py --fen=../Analysis/charlotte-gm-2020_${shard}.txt --output=../Analysis/charlotte-gm-2020_${shard}.sqlite --depth=10
done
exit 0
