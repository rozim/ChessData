ChessData
=========

PGN Mirror.
There will be dups, dirty data, errors, GM draws etc -- the data will probably need
to be post-processed, filtered, deduped etc.

# In the news:

[Command-line tools can be 235x faster than your Hadoop cluster](http://aadrake.com/command-line-tools-can-be-235x-faster-than-your-hadoop-cluster.html)

> The first thing to do is get a lot of game data. This proved more difficult than I thought it would be, but after some looking around online I found a git repository on GitHub from **rozim** that had plenty of games. I used this to compile a set of 3.46GB of data, which is about twice what Tom used in his test. The next step is to get all that data into our pipeline

# Rough notes on combining PGNs

This command should run for everyone:
nice -19 time pgn-extract -C -D -N -s -V -Z --fixresulttags --nobadresults --nosetuptags --plycount -o mega-clean.pgn */*.pgn

This is what I ran as I already had files named "mega-clean.pgn" in each subdir.
Circa 2023-12-12 there were approx 10M games and resulting file is 3.9G.
nice -19 time pgn-extract -C -D -N -s -V -Z --fixresulttags --nobadresults --nosetuptags --plycount -o mega-clean.pgn */mega-clean.pgn
      813.86 real       539.93 user       264.68 sys

## All players must be rated at least 2400
This gets rid of older games when ratings were not recorded, even for games
like world championships.

nice -19 time pgn-extract -t filter/filter-2400.txt -o mega-clean-base-2400.pgn -l log.txt < mega-clean.pgn
     655MB, 863k games
     111.70 real       105.24 user         5.01 sys

./filter.sh

# Counts

mega-clean.pgn:     5,092,808
mega-clean-2400.pgn:  808,201
mega-clean-2600.pgn:  103,658
