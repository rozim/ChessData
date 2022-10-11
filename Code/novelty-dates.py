#  Generate first date seen of positions.
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


def munch_game(game, cur_date, novelty_db):
  global n_improve, n_not_improve, n_add

  h = game.headers
  if 'FEN' in h or 'SetUp' in h:
    return None

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
        assert False, 'should be impossible now'
        novelty_db[sfen] = cur_date
      else:
        n_not_improve += 1
    except KeyError:
      if sfen == DBG:
        print('ADD ', cur_date)
      novelty_db[sfen] = cur_date
      n_add += 1



def main(argv):
  global n_add, n_improve, n_not_improve

  assert len(argv[1:]) == 1

  t0 = time.time()

  dates_db = sqlitedict.open('novelty-prep.sqlite',
                              flag='r',
                              encode=json.dumps,
                              decode=json.loads)

  novelty_db = NoveltyDb()

  pgn_fn = argv[1:][0]
  pgn_f = open(pgn_fn, 'r', encoding='utf-8', errors='replace')

  ng = 0
  dates = sorted(dates_db.keys())
  for di, date in enumerate(dates):
    if len(date) != 10:
      print('BAD LEN: ', date)
      continue
    positions = dates_db[date]
    pcd = 100.0 * di / len(dates)
    if di % 10 == 0:
      print(f'{di:6d} {date:10s} {pcd:3.1f}% {time.time() - t0:4.1f}s  np={len(positions)} ng={ng} add={n_add} imp={n_improve} ~imp={n_not_improve}')
    for pos in dates_db[date]:
      pgn_f.seek(pos, 0)
      game = chess.pgn.read_game(pgn_f)

      munch_game(game, date, novelty_db)

      fens = gen_fens(game)
      ng += 1
      if ng % 10000 == 0:
        print('\t', 'ng=', ng, f'{time.time() - t0:.1f}s #fens={len(list(fens))}')

      if ng % 100000 == 0:
        t1 = time.time()
        print('FLUSH')
        novelty_db.flush()
        dt = time.time() - t1
        print(f'FLUSHED {dt:.1f}s')

  maxrss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss // 1024 // 1024
  print('RSS: ', maxrss)
  novelty_db.flush()
  print('d1          : ', len(novelty_db.d1))
  print('d2          : ', len(novelty_db.d2))

  print('Improve     : ', n_improve)
  print('Not Improve : ', n_not_improve)
  print('Add         : ', n_add)


if __name__ == "__main__":
  app.run(main)
