# Prepare date -> list of positions to make the next stage of novelty
# calculations go faster as then we'll be sorted by date and won't ever
# have to overwrite any data.

# 4500000 97.0% 6565.9s
# 4600000 99.2% 6726.5s
# Persisting
# 0 6794.1s 15084 15084
#      6794.26 real      6758.81 user        32.11 sys
#
#

import os
import sys
import time
import collections

import chess
import chess.pgn

import sqlitedict
import json


from util import *

db = collections.defaultdict(list)
ng = 0
t0 = time.time()
for fn in sys.argv[1:]:
  print(fn)
  for gnum, (game, pct, pos) in enumerate(gen_games_pos(fn)):
    cur_date = game.headers['Date'].replace('?', '9')
    if len(cur_date) > 10:
      cur_date = cur_date[0:10]
    db[cur_date].append(pos)
    if gnum % 100000 == 0:
      print(f'{gnum} {100*pct:.1f}% {time.time()-t0:.1f}s')

print('Persisting')
sdb = sqlitedict.open('novelty-prep.sqlite',
                      flag='c',
                      encode=json.dumps,
                      decode=json.loads)

for row, (n, v) in enumerate(db.items()):
  sdb[n] = v
  if row % 100 == 0:
    sdb.sync()

sdb.sync()

dt = time.time() - t0
print(f'{ng} {dt:.1f}s {len(db)} {len(sdb)}')
