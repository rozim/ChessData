

for fn in fix-twic1025*.pgn
do
  polyglot_14/src/polyglot make-book -pgn $fn -bin polyglot.bin -max-ply 10 -min-game 1 
  rm -f polyglot.bin
done
