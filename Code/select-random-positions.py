# Pick random though unique positions out of PGN files by
# considering one position for inclusion from every game.

import logging
import os
import random
import sys
import time

import chess
import chess.pgn

from absl import app
from absl import flags

from util import *

FLAGS = flags.FLAGS

flags.DEFINE_integer('n', 10, '')
flags.DEFINE_integer('min_ply', 2, '')


def main(argv):
  sampled = [''] * FLAGS.n

  short = 0
  t0 = time.time()
  fn_random = random.random
  fn_randint = random.randint
  fn_choice = random.choice
  for fn in argv[1:]:
    print('FN: ', fn)
    for gnum, (game, pct) in enumerate(gen_games(fn)):
      if gnum % 5000 == 0:
        dt = time.time() - t0
        print(gnum, f'{dt:.1f}s')

      fens = list(gen_fens(game))
      if len(fens) < FLAGS.min_ply:
        short += 1
        continue
      slot = -1
      if gnum < FLAGS.n:
        slot = gnum
      elif fn_random() < (FLAGS.n / (1.0 + gnum)):
        slot = fn_randint(0, FLAGS.n - 1)

      if slot >= 0:
        fen = fn_choice(fens)
        sfen = ' '.join(fen.split(' ')[0:4])
        if sfen not in sampled:
          sampled[slot] = sfen

  print(f'short: {short}')
  print(f'good: {len(sampled)}')
  print()
  print('\n'.join(sampled))



if __name__ == "__main__":
  app.run(main)
