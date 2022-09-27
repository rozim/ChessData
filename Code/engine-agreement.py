import sys
import os
import json
from pprint import pprint

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


def study_game(game, db, details):
  headers = game.headers
  white = headers['White']
  white_elo = headers['WhiteElo']
  black = headers['Black']
  black_elo = headers['BlackElo']
  details.write(f'Game: {white} ({white_elo}) vs {black} ({black_elo})\n')


  sfen = None
  ply = 0
  color_played_best = {WHITE: 0, BLACK: 0}
  color_num_moves = {WHITE: 0, BLACK: 0}
  for ply, move, board in gen_moves(game):
    if len(list(board.legal_moves)) == 1:
      details.write('FORCED\n')
      continue
    if ply < FLAGS.min_ply or (FLAGS.max_ply and ply > FLAGS.max_ply):
      continue

    sfen = ' '.join(board.fen().split(' ')[0:4])
    matched = []
    played = move.uci()
    match_depth = None
    best16 = db[f'{sfen}|16'][0]['pv'][0]

    color_num_moves[board.turn] += 1
    for depth in range(0, 16 + 1):
      key = f'{sfen}|{depth}'
      analysis = db[key][0]
      ev = analysis['ev']
      best = analysis['pv'][0]
      nodes = analysis['nodes']
      if best == played:
        if depth == 16:
          color_played_best[board.turn] += 1
        matched.append('*')
        if match_depth is None:
          match_depth = depth
      else:
        matched.append(' ')
    if board.turn:
      wb = 'w'
    else:
      wb = 'b'

    details.write(f'{ply}, {wb}, {played}, {best16}, {match_depth}\n')


  if sfen is None and ply == 0:
    return
  wbest = color_played_best[WHITE]
  wnum = color_num_moves[WHITE]
  bbest = color_played_best[BLACK]
  bnum = color_num_moves[BLACK]
  print(f'Game: {white:24s} ({white_elo}) vs {black:24s} ({black_elo}) : {wbest}/{wnum} : {bbest}/{bnum}')

  return {
    white : (wbest, wnum),
    black : (bbest, bnum)}



def main(argv):
  del argv
  assert os.access(FLAGS.pgn, os.R_OK)
  assert os.access(FLAGS.reference, os.R_OK)

  db = sqlitedict.open(filename=FLAGS.reference,
                       flag='c',
                       encode=json.dumps,
                       decode=json.loads)

  xall = {}
  with open('engine-agreement-details.txt', 'w') as details:
    for game in gen_games(FLAGS.pgn):
      res = study_game(game, db, details)
      if res is None:
        continue

      for n, (best, num) in res.items():
        if n in xall:
          xall[n]['best'] += best
          xall[n]['num'] += num
        else:
          print('new', n, best, num)
          xall[n] = {'best': best, 'num': num}
  print()
  #pprint(xall)
  for name, d in xall.items():
    best = d['best']
    num = d['num']
    if num == 0:
      pct = 0
    else:
      pct = int(100.0 * (best / num))
    print(f'{name:24s} {best:4d} {num:4d} {pct:3d}%')






if __name__ == "__main__":
  app.run(main)
