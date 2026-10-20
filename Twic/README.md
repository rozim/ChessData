
http://www.theweekinchess.com/twic

update doit.sh

# download
sh ./doit.sh | sh -x

sh ./fixit.sh > shh 2> err

# slow, 5 mins
./pgn-cleanup-inplace.sh twic*.pgn

# Older (pre-2023):
  # cat fix*.pgn > fixed.pgn
  # nice -19 time polyglot make-book -pgn fixed.pgn -bin polyglot.bin -max-ply 30 -min-game 5
  # rm -f fixed.pgn

git add twic*.pgn

git commit -m "periodic update" twic*.pgn *.md *.sh
git push origin master

# Note: this is not pushed to github
time pgn-extract -C -D -N -s -V -Z --fixresulttags --nobadresults --nosetuptags --plycount -o mega-clean.pgn twic*.pgn
# 2026-10-19 time :        550.81 real       347.23 user       197.28 sys

# Regenerate mega-2400.pgn - 10 mins
./do2400.sh
# Regenerate mega-2600.pgn - 1 min
./do2600.sh
