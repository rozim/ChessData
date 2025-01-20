#!/bin/sh

exec pgn-extract -C -D -N -s -V -Z --fixresulttags --nobadresults --nosetuptags $*


# -C : no comments
# -D : no dups
# -N : no NAGs
# -V : no variations
# -s : silent
# -Z : virtual.tmp
# -fixresulttags :
# -nobadresults :
# -nosetuptags
