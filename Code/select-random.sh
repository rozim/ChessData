
dir=../Release/2022-10-05
prefix=twic-mega-clean-

python -u select-random-positions.py --n=1000 --btm --min_score=-150 --max_score=-11  ../Twic/mega-clean.pgn > ${dir}/${prefix}-btm-150-11.txt &
python -u select-random-positions.py --n=1000 --wtm --min_score=11   --max_score=150  ../Twic/mega-clean.pgn > ${dir}/${prefix}-wtm-150-11.txt &
python -u select-random-positions.py --n=1000 --btm --min_score=-10  --max_score=10   ../Twic/mega-clean.pgn > ${dir}/${prefix}-btm-10-10.txt &
python -u select-random-positions.py --n=1000 --wtm --min_score=-10  --max_score=10   ../Twic/mega-clean.pgn > ${dir}/${prefix}-wtm-10-10.txt
