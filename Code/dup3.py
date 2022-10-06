# Experimental code to look for dups based on last 3 positions in a game,
# based on what SCID does.

import sys
import os
import chess
import chess.pgn
from pprint import pprint
import time
import hashlib
import timeit
import array
import numpy as np


MIN_PLY = 19

all3 = set()
dict3 = {}

def munch_game(game):
  h = game.headers
  if 'FEN' in h or 'SetUp' in h:
    return None

  last3 = [0, 0, 0]
  board = chess.Board()
  ply = 0
  sfen = None
  for ply, move in enumerate(game.mainline_moves()):
    board.push(move)
    sfen = board.fen().split(' ')[0]
    last3[ply % 3] = hash(sfen)
  return last3, ply, sfen


def gen_games(fn):
  with open(fn, 'r', encoding='utf-8', errors='replace') as f:
    while True:
      game = chess.pgn.read_game(f)
      if game is None:
        return
      yield game


def uci(game):
  res = []
  board = chess.Board()
  for ply, move in enumerate(game.mainline_moves()):
    res.append(move.uci())
    board.push(move)
  return ' '.join(res)

def san(game):
  res = []
  board = chess.Board()
  for ply, move in enumerate(game.mainline_moves()):
    res.append(board.san(move))
    board.push(move)
  return ' '.join(res)


def munch_file(fn):
  good = 0
  dups = 0
  short = 0
  for game in gen_games(fn):
    ghashes, ply, final_sfen = munch_game(game)
    if ply < MIN_PLY:
      short += 1
      continue
    dup = False
    for ghash in ghashes:
      if ghash == 0:
        continue
      if ghash in all3:
        dups += 1
        print('dup: ', ply, game.headers)
        print(uci(game))
        print(san(game))
        print('final: ', final_sfen)
        print(dict3[ghash])
        print()
        dup = True
      all3.add(ghash)
      dict3[ghash] = game.headers
    if dup:
      dups += 1
    else:
      good += 1
  print('good: ', good, 'dups: ', dups, 'short: ', short, 'all3: ', 'all3: ', len(all3))




def main():
  for fn in sys.argv[1:]:
    t1 = time.time()
    munch_file(fn)
    dt = time.time() - t1
    print(fn, f'{dt:.1f}s')

if __name__ == '__main__':
  main()
