
http://www.theweekinchess.com/twic

update doit.sh

# download
sh ./doit.sh | sh -x

sh ./fixit.sh

./pgn-cleanup-inplace.sh twic*.pgn

cat fix*.pgn > fixed.pgn

nice -19 time polyglot make-book -pgn fixed.pgn -bin polyglot.bin -max-ply 30 -min-game 5

rm -f fixed.pgn

git add *.pgn

git commit -m "periodic update" *.pgn *.md *.sh
git push origin master
