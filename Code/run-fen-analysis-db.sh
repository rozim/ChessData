set -e
# sinqcup22

seq 0 9 | \
    xargs -P 4 -I % -t python -u fen-analysis-db.py --fen=../Analysis/$1_%.txt \
	  --output=../Analysis/pv1/$1_%.sqlite \
	  --reference=../Analysis/pv1/mega.sqlite > $1.txt \
	  --depth=16
