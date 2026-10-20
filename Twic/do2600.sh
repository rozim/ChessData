pgn-extract -t../filter/tags2600.txt \
 -D \
 -N \
 -s \
 -V  \
 -Z  \
 --fixresulttags \
 --nobadresults \
 --nosetuptags \
twic*.pgn > mega2600.pgn 2> err
