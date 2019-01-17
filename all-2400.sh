#!/bin/bash -e
set -e
set -u



rm -f mega2400*.pgn */mega2400*.pgn
rm -f mega2400*.err */mega2400*.err

for d in RebelSite Convekta Kingbase Britbase PgnMentor ChessNostalgia.com WorldChampionships Corus ChessOk.com PgnDownloads Chessopolis.com Twic Npollock Bundesliga; do
    echo $d

    files=$(ls ${d}/*.pgn | grep -v mega)
    time ./pe2400.sh ${files} > ${d}/prelim2400.pgn 2> ${d}/prelim2400.err
    # kludge -- want to do elo >= 2400 and elo < 3000
    time ./pe3000.sh ${d}/prelim2400.pgn > ${d}/mega2400.pgn 2> ${d}/mega2400.err
    time python Code/xsplit.py ${d}/mega2400.pgn
    echo " "
done
echo " "

echo FINAL
time ./pe2400.sh */mega2400*.pgn > prelim2400.pgn 2> prelim2400.err
echo FINALb
time ./pe3000.sh prelim2400.pgn > mega2400.pgn 2> mega2400.err

echo SPLIT
time python Code/xsplit.py mega2400.pgn */mega2400.pgn

git add mega2400*.pgn */mega2400*.pgn
git commit -m "mega2400 update" mega2400*.pgn */mega2400*.pgn
