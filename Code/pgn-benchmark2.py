import os
import sys
import time


import chess
import chess.pgn


from util import *


g = 0
nf = 0
t1 = time.time()
for fn in sys.argv[1:]:
  print(fn)
  for game, _ in gen_games(fn):
    g += 1
    nf += len(list(gen_fens(game)))
dt = time.time() - t1
print(f'{g} {nf} {dt:.1f}s')
