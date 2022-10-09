import sys
import os
import chess
import chess.pgn
from pprint import pprint
import time
import collections
from util import *
import resource

from absl import app
from absl import flags

FLAGS = flags.FLAGS

flags.DEFINE_integer('min_ply', 19, 'Starting ply')
flags.DEFINE_integer('max_ply', 19, 'Ending ply')
flags.DEFINE_integer('min_freq', 10, '')


def munch_game(game):
  h = game.headers
  if 'FEN' in h or 'SetUp' in h:
    return None

  board = chess.Board()
  pos = set()
  for ply, move in enumerate(game.mainline_moves()):
    board.push(move)
    if ply < FLAGS.min_ply:
      continue
    if ply > FLAGS.max_ply:
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
      print('\t', gnum, f'{100.0 * pct:.2f}% {dt:.1f}s', len(counts))

  return counts


def main(argv):
  assert FLAGS.max_ply >= FLAGS.min_ply

  counts = collections.Counter()
  for fn in argv[1:]:
    t1 = time.time()
    counts.update(munch_file(fn))
    dt = time.time() - t1
    print('fn: ', fn, len(counts), f'{dt:.1f}s')

  print('Done: ', len(counts))
  maxrss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss // 1024 // 1024
  print('RSS: ', maxrss)

  for n in sorted(counts, key=counts.get, reverse=True):
    if counts[n] >= FLAGS.min_freq:
      print(f'{n},{counts[n]}')


if __name__ == "__main__":
  app.run(main)
