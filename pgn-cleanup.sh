

dirs="Convekta RebelSite Kingbase Britbase PgnMentor ChessNostalgia.com WorldChampionships Corus ChessOk.com PgnDownloads Chessopolis.com Twic Npollock Bundesliga"
dirs=Twic
for d in "${dirs}"; do
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
		mv tmp.pgn ${f}
		git commit -m 'pgn-cleanup' ${f} > /dev/null 2>&1 < /dev/null
	esac
  done
done
