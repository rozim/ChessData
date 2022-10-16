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
flags.DEFINE_string('engine', './stockfish', '')
flags.DEFINE_string('db', '', 'Optional database name')

flags.DEFINE_integer('depth', 1, '')
flags.DEFINE_integer('multipv', 1, '')

flags.mark_flag_as_required('pgn')

HASH = 512
THREADS = 1


def main(_argv):
  assert os.access(FLAGS.pgn, os.R_OK)
  assert FLAGS.multipv >= 1
  db = None
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
  for game in gen_games(FLAGS.pgn):
    for uci, san, ply, board in gen_moves(game):
      engine.configure({"Clear Hash": None})
      sfen = simplify_fen(board)
      key = f'{sfen}|{FLAGS.depth}'
      t1 = time.time()
      try:
        multi = db[key]
      except (KeyError, TypeError):
        multi = engine.analyse(board, chess.engine.Limit(depth=FLAGS.depth), multipv=FLAGS.multipv)
        multi = list(simplify_multi(multi, board))

        if FLAGS.db:
          db[key] = multi
          n_write += 1

      dt = time.time() - t1

      if FLAGS.multipv == 1:
        ev = multi[0]['ev']
        nodes = multi[0]['nodes']
        pv = multi[0]['pv']
        pv_san = board.san(chess.Move.from_uci(pv[0]))
        print(f'{ply:3d} {san:8s} {pv_san:8s} {ev:8d} {nodes:8d} {dt:4.1f}s ')
      else:
        print(ply, san, f'{dt:.1f}s')
        for m in multi:
          print('\t', m)
  dt = time.time() - t0
  print(f'Total {dt:.1f}s')
  if FLAGS.db:
    print(f'N_Write: {n_write}')
    db.commit()
  engine.quit()


if __name__ == "__main__":
  app.run(main)
