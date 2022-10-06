import sys
import os
import chess
import chess.pgn
from pprint import pprint
import time
import collections
from util import *

MIN_PLY = 19
MAX_PLY = 60
MIN_FREQ = 10

def munch_game(game):
  h = game.headers
  if 'FEN' in h or 'SetUp' in h:
    return None

  board = chess.Board()
  pos = set()
  for ply, move in enumerate(game.mainline_moves()):
    board.push(move)
    if ply < MIN_PLY:
      continue
    if ply > MAX_PLY:
      break
    pos.add(simplify_fen(board))
  return pos


def munch_file(fn):
  counts = collections.Counter()
  t1 = time.time()
  for gnum, (g, pct) in enumerate(gen_games(fn)):
    counts.update(munch_game(g))
    if gnum % 25000 == 0:
      dt = time.time() - t1
      print(gnum, f'{100.0 * pct:.2f} {dt:.1f}s', len(counts))
  dt = time.time() - t1
  print(fn, len(counts), f'{dt:.1f}s')
  return counts


counts = collections.Counter()
for fn in sys.argv[1:]:
  counts.update(munch_file(fn))

print('Done: ', len(counts))

for n, v in counts.items():
  if v < MIN_FREQ:
    continue
  print(f'{n},{v}')
