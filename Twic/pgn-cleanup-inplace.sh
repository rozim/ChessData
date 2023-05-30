#!/bin/bash -e

for fn in $*; do
    pgn-extract \
 -C \
 -D \
 -N \
 -s \
 -V  \
 -Z  \
 --fixresulttags \
 --nobadresults \
 --nosetuptags \
"${fn}" > /tmp/$$.pgn


if cmp -s "${fn}" /tmp/$$.pgn; then
    echo SAME "${fn}"
else
    echo DIFFERENT "${fn}"
    mv /tmp/$$.pgn "${fn}"
fi
rm -f /tmp/$$.pgn
done
