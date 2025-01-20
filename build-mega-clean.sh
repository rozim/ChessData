for d in Convekta RebelSite Kingbase Britbase PgnMentor ChessNostalgia.com WorldChampionships Corus ChessOk.com PgnDownloads Chessopolis.com Twic Npollock Bundesliga; do
    echo $d
    # pgn-extract -C -D -N -s -V -Z --fixresulttags --nobadresults --nosetuptags ${d}/*.pgn > ${d}/mega-clean.sh 2> ${d}/err.txt
   sh -x ./pgn-extract.sh $(ls ${d}/*.pgn | grep -v mega) > ${d}/mega-clean.pgn 2> ${d}/err.txt
done

sh -x ./pgn-extract.sh Convekta/mega-clean.pgn RebelSite/mega-clean.pgn Kingbase/mega-clean.pgn Britbase/mega-clean.pgn PgnMentor/mega-clean.pgn ChessNostalgia.com/mega-clean.pgn WorldChampionships/mega-clean.pgn Corus/mega-clean.pgn ChessOk.com/mega-clean.pgn PgnDownloads/mega-clean.pgn Chessopolis.com/mega-clean.pgn Twic/mega-clean.pgn Npollock/mega-clean.pgn Bundesliga/mega-clean.pgn > mega-clean.pgn 2> err.txt
