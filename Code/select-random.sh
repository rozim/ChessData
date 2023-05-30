#!/bin/bash

dir=../Release/2022-10-05
prefix=twic-v2

input=../Twic/twic14*.pgn
n=1000
python -u select-random-positions.py --n=${n} --btm --min_score=-150 --max_score=-26  ${input} > ${dir}/${prefix}-btm-150-26.txt &
python -u select-random-positions.py --n=${n} --wtm --min_score=26   --max_score=150  ${input} > ${dir}/${prefix}-wtm-150-26.txt &
python -u select-random-positions.py --n=${n} --btm --min_score=-25  --max_score=25   ${input} > ${dir}/${prefix}-btm-25-25.txt &
python -u select-random-positions.py --n=${n} --wtm --min_score=-25  --max_score=25   ${input} > ${dir}/${prefix}-wtm-25-25.txt
wait
wait
wait
