# Pick random though unique positions out of PGN files by
# considering one position for inclusion from every game.
# Does not add engine analysis - see select-random-positions.py.
#
# No filtering - assume either not needed, or will be done when
# preparing PGN input (e.g. by pgn-extract).

# No wtm/btm filters, assume not needed.

import logging
import os
import random
import sys
import time

import chess
from chess import WHITE, BLACK
import chess.pgn

from absl import app
from absl import flags

from util import *

FLAGS = flags.FLAGS

flags.DEFINE_integer('n', 10, 'Number to select')
flags.DEFINE_string('pgn', '', 'input')

n_forfeit, n_good, n_already = 0, 0, 0
already = set()


def reservoir_sampler(iterable, n):
  """
    Returns @param n random items from @param iterable.
    """
  reservoir = []
  for t, item in enumerate(iterable):
    if t < n:
      reservoir.append(item)
    else:
      m = random.randint(0, t)
      if m < n:
        reservoir[m] = item
  return reservoir


def gen_one_position_per_game(fn):
  global n_forfeit, n_good, n_already, already
  t1 = time.time()
  ng = 0

  for game, pct in gen_games(fn):
    ng += 1
    if ng % 10000 == 0:
      dt = time.time() - t1
      sys.stderr.write(f'ng={ng} dt={dt:.1f} a={len(already)} pct={100.0*pct:.4f}%\n')
    fens = list(gen_fens(game))
    if len(fens) <= 1:
      n_forfeit += 1
      continue # Forfeit

    fen = random.choice(fens[:-1]) # final position may be mate so don't pick it
    board = chess.Board(fen)
    sfen = ' '.join(fen.split(' ')[0:4])
    if sfen in already:
      n_already += 1
      continue
    yield sfen
    n_good += 1
    already.add(sfen)


def main(argv):
  print('\n'.join(reservoir_sampler(gen_one_position_per_game(FLAGS.pgn), FLAGS.n)))
  sys.stderr.write(f'n_already  {n_already}\n')
  sys.stderr.write(f'n_good     {n_good}\n')
  sys.stderr.write(f'n_forfeit  {n_forfeit}\n')


if __name__ == "__main__":
  app.run(main)
