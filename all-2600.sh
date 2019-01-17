#!/bin/bash -e


rm -f mega2600*.pgn */mega2600*.pgn
rm -f mega2600*.err */mega2600*.err

for d in RebelSite Convekta Kingbase Britbase PgnMentor ChessNostalgia.com WorldChampionships Corus ChessOk.com PgnDownloads Chessopolis.com Twic Npollock Bundesliga; do
    echo $d ${d}/mega*.pgn
    rm -f ${d}/mega*.pgn
    time ./pe2600.sh ${d}/*.pgn > ${d}/prelim2600.pgn 2> ${d}/prelim2600.err
    # kludge -- want to do elo >= 2600 and elo < 3000
    time ./pe3000.sh ${d}/prelim2600.pgn > ${d}/mega2600.pgn 2> ${d}/mega2600.err
    time python Code/xsplit.py ${d}/mega2600.pgn
    echo " "
done
echo " "

echo FINAL
time ./pe2600.sh */mega2600*.pgn > prelim2600.pgn 2> prelim2600.err
echo FINALb
time ./pe3000.sh prelim2600.pgn > mega2600.pgn 2> mega2600.err

echo SPLIT
time python Code/xsplit.py mega2600.pgn */mega2600.pgn

git add mega2600*.pgn */mega2600*.pgn
git commit -m "mega2600 update" mega2600*.pgn */mega2600*.pgn
