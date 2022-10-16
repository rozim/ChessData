# Pick random though unique positions out of PGN files by
# considering one position for inclusion from every game.

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

flags.DEFINE_integer('n', 10, '')
flags.DEFINE_integer('min_ply', 2, '')
flags.DEFINE_integer('min_score', -150, 'Inclusive')
flags.DEFINE_integer('max_score', 150, 'Inclusive')
flags.DEFINE_bool('wtm', False, '')
flags.DEFINE_bool('btm', False, '')

HASH = 512
THREADS = 1 # reproducible

def main(argv):
  assert FLAGS.wtm or FLAGS.btm
  assert FLAGS.max_score >= FLAGS.min_score

  t0 = time.time()
  fn_choice = random.choice

  n_good, n_mate, n_already, n_range, n_short, n_turn = 0, 0, 0, 0, 0, 0

  engine = chess.engine.SimpleEngine.popen_uci('./stockfish')
  engine.configure({"Hash": HASH})
  engine.configure({"Threads": THREADS})

  locations = []
  for fn in argv[1:]:
    sys.stderr.write(f'Open {fn} {len(locations)}\n')
    #print('FN: ', fn)
    for _, _, pos in gen_games_pos(fn):
      locations.append((fn, pos))
  random.shuffle(locations)
  sys.stderr.write(f'LOCS: {len(locations)}\n')

  already = set()

  for gnum, (fn, pos) in enumerate(locations):
    if gnum % 1000 == 0:
      sys.stderr.write(f'{gnum} a={len(already)} g={n_good}/{FLAGS.n} m={n_mate} r={n_range} na={n_already} s={n_short}\n')
    f = open(fn, 'r', encoding='utf-8', errors='replace')
    f.seek(pos, 0)
    game = chess.pgn.read_game(f)
    f.close()

    fens = list(gen_fens(game))
    if len(fens) < FLAGS.min_ply:
      n_short += 1
      continue
    fen = fn_choice(fens[:-1]) # final position may be mate so don't pick it

    engine.configure({"Clear Hash": None})
    board = chess.Board(fen)
    if ((FLAGS.wtm and board.turn == WHITE) or
        (FLAGS.btm and board.turn == BLACK)):
      pass
    else:
      n_turn += 1
      continue
    m = engine.analyse(board, chess.engine.Limit(depth=1))
    is_mate, score = simplify_score2(m['score'])
    if is_mate:
      n_mate += 1
      continue
    elif score < FLAGS.min_score or score > FLAGS.max_score:
      n_range += 1
      continue
    sfen = ' '.join(fen.split(' ')[0:4])
    if sfen in already:
      n_already += 1
      continue
    print(sfen)
    n_good += 1
    already.add(sfen)
    if n_good >= FLAGS.n:
      sys.stderr.write(f'break {n_good} {FLAGS.n}\n')
      break

  engine.quit()

  sys.stderr.write(f'gnum       {gnum}\n')
  sys.stderr.write(f'already    {len(already)}\n')
  sys.stderr.write(f'n_good     {n_good}\n')
  sys.stderr.write(f'n_turn     {n_turn}\n')
  sys.stderr.write(f'n_already  {n_already}\n')
  sys.stderr.write(f'n_mate     {n_mate}\n')
  sys.stderr.write(f'n_range    {n_range}\n')
  sys.stderr.write(f'n_short    {n_short}\n')


if __name__ == "__main__":
  app.run(main)
