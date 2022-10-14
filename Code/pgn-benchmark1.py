# gen_games

# python pgn-benchmark1.py ../ChessOk.com/mega-clean.pgn
# 465587 623.4s


# /Users/dave/Downloads/pypy-c-jit-106225-39ac625a6e2a-macos_arm64/bin/pypy3 pgn-benchmark1.py ../ChessOk.com/mega-clean.pgn
# 460000 460000 98.8% 460.0s
# 465587 465.4s
#
# 75% of the earlier time

import os
import sys
import time


import chess
import chess.pgn


from util import *


ng = 0
t1 = time.time()
for fn in sys.argv[1:]:
  print(fn)
  for gnum, (g, pct) in enumerate(gen_games(fn)):
    if gnum % 10000 == 0:
      print(f'{gnum} {ng} {pct*100:.1f}% {time.time()-t1:.1f}s')
      if gnum >= 30000:
        break
    ng += 1

dt = time.time() - t1
print(f'{ng} {dt:.1f}s')
