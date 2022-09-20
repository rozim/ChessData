seq 1 2 | xargs -P 1 -I % echo python -u fen-analysis-db.py --fen=../Analysis/charlotte-gm-2020_%.txt --output=../Analysis/charlotte-gm-2020_%.sqlite --depth=11 --reference=../Analysis/mega.sqlite
