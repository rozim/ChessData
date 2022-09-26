

for d in 0 1 2 3 4 5 6 7 8 9 10
do
    python match.py --depth=${d} --second=False --num_matches=0  > d${d}-false.txt 2>&1
    python match.py --depth=${d} --second=True  --num_matches=0  > d${d}-true.txt 2>&1
done
