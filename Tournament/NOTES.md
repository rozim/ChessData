
pgn-extract -t kvika-open-tag.txt -C -D -N -s -V -Z --fixresulttags --nobadresults --nosetuptags --plycount -o kvika-open-clean.pgn ../Twic/twic1431.pgn ../Twic/twic1432.pgn

python gen-fen.py --pgn=../Tournament/kvika-open-hans-clean.pgn  --prefix=../Analysis/pv1/kvika-open-hans  --n=1

python fen-analysis-db.py --fen=../Analysis/pv1/kvika-open-hans_0.txt --output=../Analysis/pv1/kvika-open-hans.sqlite --reference=../Analysis/pv1/mega.sqlite --depth=16
