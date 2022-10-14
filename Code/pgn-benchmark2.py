# gen_games then gen_fens

import os
import sys
import time

# python pgn-benchmark2.py ../ChessOk.com/mega-clean.pgn
# 465587 38433474 2096.6s
# ng     nf
#
# 222 games/sec
# 18336 fens/sec
#
#


import chess
import chess.pgn

from util import *


ng = 0
nf = 0
t1 = time.time()
for fn in sys.argv[1:]:
  print(fn)
  for gnum, (game, pct) in enumerate(gen_games(fn)):
    if gnum % 1000 == 0:
      print(f'{gnum} {ng} {pct*100:.1f}% {time.time()-t1:.1f}s')
    ng += 1
    nf += len(list(gen_fens(game)))
dt = time.time() - t1
print(f'{ng} {nf} {dt:.1f}s')
