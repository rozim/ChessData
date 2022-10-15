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
flags.DEFINE_integer('min_score', -150, 'Inclusive')
flags.DEFINE_integer('max_score', 150, 'Inclusive')

HASH = 512
THREADS = 1 # reproducible

def main(argv):
  t0 = time.time()
  fn_choice = random.choice

  engine = chess.engine.SimpleEngine.popen_uci('stockfish')
  engine.configure({"Hash": HASH})
  engine.configure({"Threads": THREADS})

  locations = []
  for fn in argv[1:]:
    #print('FN: ', fn)
    for _, _, pos in gen_games_pos(fn):
      locations.append((fn, pos))
  random.shuffle(locations)
  sys.stderr.write(f'LOCS: {len(locations)}\n')

  already = set()
  good = 0
  for gnum, (fn, pos) in enumerate(locations):
    if gnum % 1000 == 0:
      sys.stderr.write(f'{gnum}\n')
    f = open(fn, 'r', encoding='utf-8', errors='replace')
    f.seek(pos, 0)
    game = chess.pgn.read_game(f)
    f.close()

    fens = list(gen_fens(game))
    if len(fens) < FLAGS.min_ply:
      continue
    fen = fn_choice(fens[:-1]) # final position may be mate so don't pick it

    engine.configure({"Clear Hash": None})
    m = engine.analyse(chess.Board(fen), chess.engine.Limit(depth=0))
    is_mate, score = simplify_score2(m['score'])
    if is_mate:
      continue
    elif score < FLAGS.min_score or score > FLAGS.max_score:
      continue
    sfen = ' '.join(fen.split(' ')[0:4])
    if sfen not in already:
      print(sfen)
      already.add(sfen)
      good += 1
      if good >= FLAGS.n:
        break

  engine.quit()



if __name__ == "__main__":
  app.run(main)
