This is an attempt to aggregate and dedup the content here and filter out games that are
probably not useful.

The filtering tool is (source: TBD). It looks for games with somewhat
reasonable PGN headers, games that are not of low quality (e.g bullet),
games that are not obviously computer vs computer matches, and games where
neither player has a rating < 2200. Games, esp older ones, where neither
player is rated get though.

The files are sized at around 50MB to make GitHub happy.

These were generated on 26-Dec-2015.
Stats are:

        Games     :  4573570  (total PGN games stated with)
        Final pos :  2189096  (how many we ended with after passing the filtering)
        Dup games :  2384474  (approx # of deups)
        Rejection reasons
        Too short :    14707  (games < 10 ply)
        Bad result:      653  (games w/o a proper result tag)
        Bad header:  1360450
        Dup[0]    :  2339184  (games where the last position is a dup)
        Dup[1]    :    30583  (games where the next to last pos matches one of the last 3 in another game)
        Dup[2]    :    31462  (similar..)

To use of course concat filter_??.pgn if you want one big file.

2 opening books based on these files.
The books were made as follows:

cat filtered_??.pgn > /tmp/filtered.pgn
./polyglot make-book -pgn /tmp/filtered.pgn  -bin filtered-book-popularity.bin -max-ply 40 -min-game 5
./polyglot make-book -pgn /tmp/filtered.pgn  -bin filtered-book-uniform.bin    -max-ply 40 -min-game 5 -uniform