# Analyze a PGN file to a single depth.
import json
import logging
import os
import sys
import time

import chess
import chess.pgn
from chess import WHITE, BLACK
import chess.engine

from absl import app
from absl import flags

import sqlitedict

from util import *

FLAGS = flags.FLAGS
flags.DEFINE_string('pgn', None, 'PGN input file')
flags.DEFINE_string('engine', 'stockfish', '')
flags.DEFINE_integer('min_ply', 20, 'Starting ply')
flags.DEFINE_integer('max_ply', 120, 'Ending ply')
flags.DEFINE_string('db', None, 'Optional database name')

flags.DEFINE_integer('min_depth', 0, '')
flags.DEFINE_integer('max_depth', 10, '')
flags.DEFINE_integer('multipv', 1, '')

flags.mark_flag_as_required('pgn')
flags.mark_flag_as_required('db')

HASH = 512
THREADS = 1


def main(_argv):
  assert os.access(FLAGS.pgn, os.R_OK)
  assert FLAGS.multipv >= 1

  if FLAGS.db:
    print(f'Opening {FLAGS.db}')
    db = sqlitedict.open(filename=FLAGS.db,
                         flag='c',
                         encode=json.dumps,
                         decode=json.loads)
    print(f'Rows {len(db)}')

  engine = chess.engine.SimpleEngine.popen_uci(FLAGS.engine)
  engine.configure({"Hash": HASH})
  engine.configure({"Threads": THREADS})

  n_write, n_cache = 0, 0
  t0 = time.time()

  for gnum, (game, pct) in enumerate(gen_games(FLAGS.pgn)):
    t1 = time.time()
    headers = game.headers
    white = headers['White']
    black = headers['Black']
    result = headers['Result']
    for uci, san, ply, board in gen_moves(game):
      actions = 0
      if len(list(board.legal_moves)) == 1:
        continue # Forced, only move
      if ply < FLAGS.min_ply or (FLAGS.max_ply and ply > FLAGS.max_ply):
        continue

      sfen = simplify_fen(board)

      for depth in range(FLAGS.min_depth, FLAGS.max_depth):
        engine.configure({"Clear Hash": None})
        key = f'{sfen}|{depth}'
        try:
          multi = db[key]
          n_cache += 1
        except KeyError:
          multi = engine.analyse(board, chess.engine.Limit(depth=depth), multipv=FLAGS.multipv)
          multi = list(simplify_multi(multi, board))

          db[key] = multi
          n_write += 1
          actions += 1
    db.commit()
    dt = time.time() - t1
    print(f'{(100.0 * pct):3.1f}% {gnum:4d} {white:24s} {black:24s} {result:8s} (c:{n_cache:8d} w:{n_write:8d}) p:{ply:3d} a/dt:{(actions/dt):.1f}s dt:{dt:.1f}s')

  dt = time.time() - t0
  print()
  print(f'Total {dt:.1f}s')
  print(f'Writes: {n_write}')
  print(f'Caches: {n_cache}')

  db.commit()
  engine.quit()


if __name__ == "__main__":
  app.run(main)
