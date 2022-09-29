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

  n_write = 0
  t0 = time.time()

  for gnum, game in enumerate(gen_games(FLAGS.pgn)):
    t1 = time.time()
    headers = game.headers
    white = headers['White']
    black = headers['Black']
    for uci, san, ply, board in gen_moves(game):
      if len(list(board.legal_moves)) == 1:
        continue # Forced, only move
      if ply < FLAGS.min_ply or (FLAGS.max_ply and ply > FLAGS.max_ply):
        continue

      engine.configure({"Clear Hash": None})
      sfen = simplify_fen(board)

      for depth in range(FLAGS.min_depth, FLAGS.max_depth):
        key = f'{sfen}|{depth}'
        try:
          multi = db[key]
        except KeyError:
          multi = engine.analyse(board, chess.engine.Limit(depth=depth), multipv=FLAGS.multipv)
          multi = list(simplify_multi(multi, board))

          db[key] = multi
          n_write += 1
    dt = time.time() - t0
    print(f'{gnum:4d} {white:24s} {black:24s} {dt:.1f}s')

  dt = time.time() - t0
  print(f'Total {dt:.1f}s')
  print(f'Writes: {n_write}')

  db.commit()
  engine.quit()


if __name__ == "__main__":
  app.run(main)
