import sys
import os
import json
from pprint import pprint
from dataclasses import dataclass

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
flags.DEFINE_string('output', None, 'Output sqlite')
flags.DEFINE_string('reference', None, 'Reference sqlite')
flags.DEFINE_integer('min_ply', 20, 'Starting ply')
flags.DEFINE_integer('max_ply', 120, 'Ending ply')

flags.mark_flag_as_required('pgn')


def pc(a, b):
  assert a >= 0 and b >= 0
  if b == 0:
    return 0
  return int(100.0 * (a / b))


def gen_games(fn):
  f = open(fn, 'r', encoding='utf-8', errors='replace')
  while True:
    g = chess.pgn.read_game(f)
    if g is None:
      return
    yield g


def gen_moves(game):
  board = chess.Board()

  for ply, move in enumerate(game.mainline_moves()):
    yield ply, move, board
    board.push(move)


def gen_analysis(db, board):
  sfen = ' '.join(board.fen().split(' ')[0:4])
  for depth in range(0, 16 + 1):
    key = f'{sfen}|{depth}'
    analysis = db[key][0]
    ev = analysis['ev']
    best = analysis['pv'][0]
    nodes = analysis['nodes']
    yield {'ev': ev, 'best': best, 'nodes': nodes}


def is_easy(analysis):
  best0 = analysis[0]['best']
  for cur in analysis[1:]:
    if best0 != cur['best']:
      return False
  return True



@dataclass
class Stats:
  name: str
  rating: int
  played_best: int = 0
  num_moves: int = 0
  played_easy: int = 0
  missed_easy: int = 0

  def combine(self, other):
    self.played_best += other.played_best
    self.played_easy += other.played_easy
    self.missed_easy += other.missed_easy
    self.num_moves += other.num_moves


def study_game(game, db, details):
  headers = game.headers
  white = headers['White']
  white_elo = headers['WhiteElo']
  black = headers['Black']
  black_elo = headers['BlackElo']

  details.write(f'Game: {white} ({white_elo}) vs {black} ({black_elo})\n')

  color_stats = {WHITE: Stats(name=white,
                              rating=white_elo),
                 BLACK: Stats(name=black,
                              rating=black_elo)}

  for ply, move, board in gen_moves(game):
    turn = board.turn
    if len(list(board.legal_moves)) == 1:
      details.write('FORCED\n')
      continue
    if ply < FLAGS.min_ply or (FLAGS.max_ply and ply > FLAGS.max_ply):
      continue

    color_stats[turn].num_moves += 1
    matched = []
    played = move.uci()
    match_depth = None
    analysis = list(gen_analysis(db, board))
    easy = is_easy(analysis)

    best16 = analysis[16]['best']
    if best16 == played:
      color_stats[turn].played_best += 1
      if easy:
        color_stats[turn].played_easy += 1
    else:
      if easy:
        color_stats[turn].missed_easy += 1

    details.write(f'{ply}, {played}, {best16}\n')

  wbest = color_stats[WHITE].played_best
  wnum = color_stats[WHITE].num_moves
  bbest = color_stats[BLACK].played_best
  bnum = color_stats[WHITE].num_moves

  print(f'Game: {white:24s} ({white_elo}) vs {black:24s} ({black_elo}) : {wbest}/{wnum} : {bbest}/{bnum}')

  # A bit of a leaky hack.
  color_stats[color_stats[WHITE].name] = color_stats[WHITE]
  color_stats[color_stats[BLACK].name] = color_stats[BLACK]
  return color_stats


def main(argv):
  del argv
  assert os.access(FLAGS.pgn, os.R_OK)
  assert os.access(FLAGS.reference, os.R_OK)

  db = sqlitedict.open(filename=FLAGS.reference,
                       flag='c',
                       encode=json.dumps,
                       decode=json.loads)

  total_stats = {}
  with open('engine-agreement-details.txt', 'w') as details:
    for game in gen_games(FLAGS.pgn):
      res_stats = study_game(game, db, details)
      white = res_stats[WHITE].name
      black = res_stats[BLACK].name

      if white in total_stats:
        total_stats[white].combine(res_stats[WHITE])
      else:
        total_stats[white] = res_stats[WHITE]

      if black in total_stats:
        total_stats[black].combine(res_stats[BLACK])
      else:
        total_stats[black] = res_stats[BLACK]


  print()
  for name, stats in total_stats.items():
    best = stats.played_best
    played_easy = stats.played_easy
    missed_easy = stats.missed_easy
    num = stats.num_moves
    pct = pc(best, num)
    pct_easy = pc(played_easy, played_easy + missed_easy)
    pct_missed_easy = pc(missed_easy, played_easy + missed_easy)
    rating = stats.rating
    print(f'{name:24s} ({rating}) {best:4d} {num:4d} {pct:3d}% | easy {pct_easy:3d}% {pct_missed_easy:3d}%')






if __name__ == "__main__":
  app.run(main)
