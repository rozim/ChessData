pgn-extract -t../filter/tags2400.txt \
 -D \
 -N \
 -s \
 -V  \
 -Z  \
 --fixresulttags \
 --nobadresults \
 --nosetuptags \
twic*.pgn > mega2400.pgn 2> err
