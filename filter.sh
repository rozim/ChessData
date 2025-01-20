

time pgn-extract --tagsubstr -t filter/filter-reject-events.txt      -n mega-clean-event.pgn      -o /dev/null  -l log1.txt < mega-clean-base-2400.pgn
time pgn-extract --tagsubstr -t filter/filter-reject-eventtypes.txt  -n mega-clean-eventtype.pgn  -o /dev/null  -l log2.txt < mega-clean-event.pgn
time pgn-extract --tagsubstr -t filter/filter-reject-players.txt     -n mega-clean-players.pgn    -o foo.pgn    -l log3.txt < mega-clean-eventtype.pgn
time pgn-extract --tagsubstr -t filter/filter-reject-sites.txt       -n mega-clean-site.pgn       -o foo2.pgn   -l log4.txt < mega-clean-players.pgn

cp mega-clean-site.pgn mega-clean-2400.pgn

time pgn-extract -t filter/filter-2600.txt -o mega-clean-2600.pgn -l log.txt < mega-clean-2400.pgn
