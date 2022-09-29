import logging
import sys
import os

import time

import chess
import chess.pgn
from chess import WHITE, BLACK
import chess.engine

from absl import app
from absl import flags

from util import *

FLAGS = flags.FLAGS
flags.DEFINE_string('pgn', None, 'PGN input file')
flags.DEFINE_string('engine', 'stockfish', '')
flags.DEFINE_integer('min_ply', 20, 'Starting ply')
flags.DEFINE_integer('max_ply', 120, 'Ending ply')

flags.DEFINE_integer('depth', 1, '')
flags.DEFINE_integer('multipv', 1, '')

flags.mark_flag_as_required('pgn')

HASH = 512
THREADS = 1


def main(_argv):
  assert os.access(FLAGS.pgn, os.R_OK)
  assert FLAGS.multipv >= 1

  engine = chess.engine.SimpleEngine.popen_uci('./stockfish')
  engine.configure({"Hash": HASH})
  engine.configure({"Threads": THREADS})
  #print(engine.options)
  t0 = time.time()
  for game in gen_games(FLAGS.pgn):
    for uci, san, ply, board in gen_moves(game):

      engine.configure({"Clear Hash": None})
      t1 = time.time()
      multi = engine.analyse(board, chess.engine.Limit(depth=FLAGS.depth), multipv=FLAGS.multipv)
      multi = list(simplify_multi(multi, board))
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
  engine.quit()


if __name__ == "__main__":
  app.run(main)
