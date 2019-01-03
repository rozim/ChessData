

for d in RebelSite Convekta Kingbase Britbase PgnMentor ChessNostalgia.com WorldChampionships Corus ChessOk.com PgnDownloads Chessopolis.com Twic Npollock Bundesliga; do
  for f in $d/*.pgn; do
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
  done
done

	
	
