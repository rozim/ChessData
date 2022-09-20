seq 1 2 | xargs -P 1 -I % echo python -u fen-analysis-db.py --fen=../Analysis/charlotte-gm-2020_%.txt --output=../Analysis/charlotte-gm-2020_%.sqlite --depth=11 --reference=../Analysis/mega.sqlite

seq 0 9 | time xargs -P 4 -I % -t python -u fen-analysis-db.py --fen=../Analysis/charlotte-gm-2020_%.txt --output=../Analysis/charlotte-gm-2020_%.sqlite --depth=10 --reference=../Analysis/mega.sqlite  > shh-10

seq 0 9 | time xargs -P 4 -I % -t python -u fen-analysis-db.py --fen=../Analysis/charlotte-gm-2020_%.txt --output=../Analysis/charlotte-gm-2020_%.sqlite --depth=13 --reference=../Analysis/mega.sqlite  > shh-13
