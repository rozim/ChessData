import sys
import os
import json
import random

import time
import sqlitedict

import chess
from chess import WHITE, BLACK
import chess.engine
import chess.pgn

from absl import app
from absl import flags

FLAGS = flags.FLAGS
flags.DEFINE_string('pgn', None, 'Input')
flags.DEFINE_string('prefix', None, 'Output')
flags.DEFINE_integer('n', 10, 'sharding')
flags.mark_flag_as_required('pgn')
flags.mark_flag_as_required('prefix')

MIN_PLY = 20
MAX_PLY = 120
MAX_GAMES = 0

def gen_games(fn):
  f = open(fn, 'r')
  while True:
    g = chess.pgn.read_game(f)
    if g is None:
      return
    yield g


def gen_moves(game):
  board = game.board()
  for move in game.mainline_moves():
    board.push(move)
    yield move, board


def simplify_fen(board):
  #rn2kbnr/ppq2pp1/4p3/2pp2Bp/2P4P/1Q6/P2NNPP1/3RK2R w Kkq - 2 13
  return ' '.join(board.fen().split(' ')[0:4])


def main(argv):
  del argv
  assert os.access(FLAGS.pgn, os.R_OK)

  already = set()

  dups = 0
  adds = 0

  fns = [f'{FLAGS.prefix}_{i:d}.txt' for i in range(FLAGS.n)]
  files = [open(fn, 'w') for fn in fns]

  for gnum, game in enumerate(gen_games(FLAGS.pgn)):
    if MAX_GAMES > 0 and gnum >= MAX_GAMES:
      break

    for ply, (move, board) in enumerate(gen_moves(game)):
      if ply < MIN_PLY or ply > MAX_PLY:
        continue
      sfen = simplify_fen(board)
      if sfen in already:
        dups += 1
        continue
      already.add(sfen)
      adds += 1

      files[random.randint(0, FLAGS.n - 1)].write(sfen + '\n')

  for f in files:
    f.close()

  print('Dups: ', dups)
  print('Adds: ', adds)
  print('Games: ', gnum)


if __name__ == "__main__":
  app.run(main)
