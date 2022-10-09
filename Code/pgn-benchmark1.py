# gen_games

#  /Users/dave/Projects/ChessData/Release/2022-10-05:
#  -r--r--r--    1 dave  staff  3442210859 Oct  5 16:35 mega-clean.pgn
#
# Time:

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
    ng += 1
dt = time.time() - t1
print(f'{ng} {dt:.1f}s')
