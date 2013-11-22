
http://www.theweekinchess.com/twic

update doit.sh

sh ./doit.sh | sh -x

sh ./fixit.sh

cat fix*.pgn > fixed.pgn

nice -19 time polyglot make-book -pgn fixed.pgn -bin polyglot.bin -max-ply 30 -min-game 5 

rm -f fixed.pgn