#!/bin/bash -e


rm -f mega2600*.pgn */mega2600*.pgn
rm -f mega2600*.err */mega2600*.err

for d in RebelSite Convekta Kingbase Britbase PgnMentor ChessNostalgia.com WorldChampionships Corus ChessOk.com PgnDownloads Chessopolis.com Twic Npollock Bundesliga; do
    echo $d ${d}/mega*.pgn
    rm -f ${d}/mega*.pgn
    time ./pe2600.sh ${d}/*.pgn > ${d}/mega2600.pgn 2> ${d}/mega2600.err
    time python Code/xsplit.py ${d}/mega2600.pgn
    echo " "
done

echo FINAL
time ./pe2600.sh */mega2600*.pgn > mega2600.pgn 2> mega2600.err

echo SPLIT
time python Code/xsplit.py mega2600.pgn */mega2600.pgn
