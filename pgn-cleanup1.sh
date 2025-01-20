
for fn in $*; do
    echo $fn
    pgn-extract -C -D -N -s -V -Z --fixresulttags --nobadresults --nosetuptags ${fn} > /tmp/$$.pgn
    mv /tmp/$$.pgn ${fn}
done
