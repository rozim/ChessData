seq 1 2 | xargs -P 1 -I % echo python -u fen-analysis-db.py
--fen=../Analysis/charlotte-gm-2020_%.txt
--output=../Analysis/charlotte-gm-2020_%.sqlite --depth=11
--reference=../Analysis/mega.sqlite

seq 0 9 | time xargs -P 4 -I % -t python -u fen-analysis-db.py
--fen=../Analysis/charlotte-gm-2020_%.txt
--output=../Analysis/charlotte-gm-2020_%.sqlite --depth=10
--reference=../Analysis/mega.sqlite > shh-10

seq 0 9 | time xargs -P 4 -I % -t python -u fen-analysis-db.py
--fen=../Analysis/charlotte-gm-2020_%.txt
--output=../Analysis/charlotte-gm-2020_%.sqlite --depth=13
--reference=../Analysis/mega.sqlite > shh-13

--------------------------------------------------------------------------------

https://cse.buffalo.edu/~regan/chess/fidelity/data/Niemann/

https://cse.buffalo.edu/~regan/chess/fidelity/data/Niemann/SigemanMay2022cat18_SF15d20-30pv1.sc4

python gen-fen.py --pgn=../Twic/twic1453.pgn --prefix=../Analysis/twic1453

./run-fen-analysis-db.sh sinqcup22 > sinqcup22.txt

python gen-fen.py --min_ply=0 --max_ply=0 --pgn=../Game/smyslov-browne-1973.pgn
--prefix=../Analysis/deep/smyslov-browne-1973.txt --n=1

-----

python gen-fen.py --pgn=../Twic/twic1352.pgn --event="CCCSA Fall GM 2020" --prefix=../Analysis/charlotte-gm-2020

cd /Users/dave/Projects/ChessData/Code
nice time python fen-analysis-db.py --fen=../Analysis/pv1/kvika-open-hans_0.txt --output=../Analysis/pv1/kvika-open-hans.sqlite --reference=../Analysis/pv1/mega.sqlite --depth=16
