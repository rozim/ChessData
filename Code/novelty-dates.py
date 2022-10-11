# Generate first date seen of positions.
import sys
import os
import chess
import chess.pgn
from pprint import pprint
import time
import collections
from util import *
import resource
import sqlitedict
import json

from absl import app
from absl import flags

FLAGS = flags.FLAGS

flags.DEFINE_integer('max_ply', 60, 'Ending ply')

n_improve = 0
n_not_improve = 0
n_add = 0
n_bad_date = 0

DBG = '3rrqk1/1p3ppp/p1bb1n2/3p4/7Q/1PN1PN2/PB3PPP/2RR2K1 b - -'

class NoveltyDb:
  def __init__(self):
    self.d1 = sqlitedict.open('novelty.sqlite',
                              flag='c',
                              encode=json.dumps,
                              decode=json.loads)
    self.d2 = {}


  def __getitem__(self, key):
    try:
      return self.d2[key]
    except KeyError:
      return self.d1[key]


  def __setitem__(self, key, value, /):
    self.d2[key] = value
    # only set self.d1 on flush()


  def flush(self):
    for k, v in self.d2.items():
      self.d1[k] = v
    self.d2 = {}
    self.d1.sync()


def munch_game(game, novelty_db):
  global n_improve, n_not_improve, n_add, n_bad_date

  h = game.headers
  if 'FEN' in h or 'SetUp' in h:
    return None
  cur_date = h['Date'].replace('?', '9')
  if len(cur_date) > 10:
    n_bad_date += 1
    cur_date = cur_date[0:10]
  # assert len(cur_date) == 10, (cur_date, h)
  # sample bad date: [Date "2022.08.22`"]

  board = chess.Board()
  for ply, move in enumerate(game.mainline_moves()):
    board.push(move)
    if ply > FLAGS.max_ply:
      break
    sfen = simplify_fen(board)
    try:
      db_date = novelty_db[sfen]
      if cur_date < db_date:
        if sfen == DBG:
          print('IMPROVE ', db_date, cur_date)
        n_improve += 1
        novelty_db[sfen] = cur_date
      else:
        n_not_improve += 1
    except KeyError:
      if sfen == DBG:
        print('ADD ', cur_date)
      novelty_db[sfen] = cur_date
      n_add += 1


def munch_file(fn, novelty_db):
  global n_add, n_improve, n_not_improve, n_bad_date
  t1 = time.time()
  for gnum, (g, pct) in enumerate(gen_games(fn)):
    munch_game(g, novelty_db)
    if gnum % 25000 == 0:
      dt = time.time() - t1
      n1 = len( novelty_db.d1)
      n2 = len( novelty_db.d2)
      print(f'\t{gnum} {100.0 * pct:.2f}% {dt:.1f}s add={n_add} improve={n_improve} | {n_not_improve} d1={n1} d2={n2}')
      if n2 > 10000000:
        print('[flush]')
        novelty_db.flush()


def main(argv):
  global n_add, n_improve, n_not_improve, n_bad_date
  novelty_db = NoveltyDb()

  for fn in argv[1:]:
    t1 = time.time()
    munch_file(fn, novelty_db)
    novelty_db.flush()
    dt = time.time() - t1
    print('fn: ', fn, f'{dt:.1f}s add={n_add} improve={n_improve} : {n_not_improve}')

  maxrss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss // 1024 // 1024
  print('RSS: ', maxrss)
  novelty_db.flush()
  print('d1          : ', len(novelty_db.d1))
  print('d2          : ', len(novelty_db.d2))

  print('Improve     : ', n_improve)
  print('Not Improve : ', n_improve)
  print('Add         : ', n_add)
  print('Bad date    : ', n_bad_date)


if __name__ == "__main__":
  app.run(main)
