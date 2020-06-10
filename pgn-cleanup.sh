
# Convekta
# for d in RebelSite  Kingbase Britbase PgnMentor ChessNostalgia.com WorldChampionships Corus ChessOk.com PgnDownloads Chessopolis.com Twic Npollock Bundesliga; do
for d in Twic; do
    for f in $d/*.pgn; do
	case $f in
	    */mega*.pgn)
		echo SKIP $f
		;;
	    *)
		echo DOIT $f
		pgn-extract \
		    -C \
		    -D \
		    -N \
		    -s \
		    -V  \
		    -Z  \
		    --fixresulttags \
		    --nobadresults \
		    --nosetuptags \
		    $f > tmp.pgn 2> tmp.err
		mv tmp.pgn $f
	esac
  done
done

	
	
