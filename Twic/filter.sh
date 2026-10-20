
set -e
time pgn-extract --tagsubstr -t filter-player.txt     -o mega-clean-player-fail.pgn    -n mega-clean-player-pass.pgn    < mega-clean.pgn              > player.out    2>&1
time pgn-extract --tagsubstr -t filter-event.txt      -o mega-clean-event-fail.pgn     -n mega-clean-event-pass.pgn     < mega-clean-player-pass.pgn  > event.out     2>&1
time pgn-extract --tagsubstr -t filter-eventtype.txt  -o mega-clean-eventtype-fail.pgn -n mega-clean-eventtype-pass.pgn < mega-clean-event-pass.pgn   > eventtype.out 2>&1
