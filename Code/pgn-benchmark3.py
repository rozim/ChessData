# Look for date

# python pgn-benchmark3.py ../ChessOk.com/mega-clean.pgn
# ../ChessOk.com/mega-clean.pgn
# lines=11264281 1.2s (raw lines)
# ../ChessOk.com/mega-clean.pgn
# dates=465587 1.6s (dates)

import os
import sys
import time


import chess
import chess.pgn


from util import *



lines = 0

t1 = time.time()
for fn in sys.argv[1:]:
  print(fn)
  with open(fn, 'r', encoding='utf-8', errors='replace') as f:
    for line in f.readlines():
      lines += 1

dt = time.time() - t1
print(f'lines={lines} {dt:.1f}s (raw lines)')

#####
# [Date "1901.11.23"]

dates = 0
t1 = time.time()
for fn in sys.argv[1:]:
  print(fn)
  with open(fn, 'r', encoding='utf-8', errors='replace') as f:
    for line in f.readlines():
      if line.startswith('[Date "'):
        dates += 1

dt = time.time() - t1
print(f'dates={dates} {dt:.1f}s (dates)')
