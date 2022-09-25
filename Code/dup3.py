# Experimental code to look for dups based on last 3 positions in a game.
import sys
import os
import chess
import chess.pgn
from pprint import pprint
import time
import collections

MIN_PLY = 20
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
    pos.add(board.fen().split(' ')[0])
  return pos


def munch_file(fn):
  counts = collections.Counter()
  t1 = time.time()
  with open(fn, 'r', encoding='utf-8', errors='replace') as f:
    while True:
      g = chess.pgn.read_game(f)
      if g is None:
        break
      counts.update(munch_game(g))
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
