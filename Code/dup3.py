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
from fuzzywuzzy import fuzz
from farmhash import FarmHash64

RATIO = 50


dict3 = {}
f_close = None
f_dup = None

def print_headers(h):
  print(h['White'], h['Black'], h['Event'], h['Site'])


def headers2s(h):
  return h['White'] + ' | ' + h['Black'] + ' | ' + h['Event'] + ' | ' + h['Site'] + '\n'


def simplify_headers(headers):
  return {name: headers[name]
          for name in ['White', 'Black', 'Event', 'Site']}


def munch_game(game):
  h = game.headers
  if 'FEN' in h or 'SetUp' in h:
    return None

  last3 = [0, 0, 0]
  board = chess.Board()
  ply = 0
  uci = []
  for ply, move in enumerate(game.mainline_moves()):
    uci.append(move.uci())
    board.push(move)

  last3[0] = FarmHash64(''.join(uci))
  last3[1] = FarmHash64(''.join(uci[0:-1]))
  last3[2] = FarmHash64(''.join(uci[0:-2]))
  return last3, ply


def gen_games(fn):
  with open(fn, 'r', encoding='utf-8', errors='replace') as f:
    while True:
      pos = f.seek(0, 1)
      game = chess.pgn.read_game(f)
      if game is None:
        return
      yield game, pos


def fuzzy_close(sheaders, xheaders):
  return (fuzz.ratio(sheaders['White'], xheaders['White']) > RATIO and
          fuzz.ratio(sheaders['Black'], xheaders['Black']) > RATIO and
          fuzz.ratio(sheaders['Event'], xheaders['Event']) > RATIO and
          fuzz.ratio(sheaders['Site'], xheaders['Site']) > RATIO)


def munch_file(fn):
  global f_close, f_dup
  good = 0
  dups = 0
  near_dups = 0


  for gnum, (game, pos) in enumerate(gen_games(fn)):
    sheaders = None
    #print(fn, pos, simplify_headers(game.headers))
    if gnum % 1000 == 0:
      f_close.flush()
      f_dup.flush()

    ghashes, max_ply = munch_game(game)

    near_dup, dup = False, False
    for ghash in ghashes:
      if dup:
        continue
      if ghash not in dict3:
        continue
      near_dup = True
      if sheaders is None:
        sheaders = simplify_headers(game.headers)

      xfn, xpos, xheaders = dict3[ghash]
      if fuzzy_close(sheaders, xheaders):
        dup = True
        f_dup.write(f'{fn}:{pos}\n')
        f_dup.write(f'{xfn}:{xpos}\n')
        f_dup.write(headers2s(sheaders))
        f_dup.write(headers2s(xheaders))
        f_dup.write('\n')

    if sheaders is None:
      sheaders = simplify_headers(game.headers)
    for ghash in ghashes:
      if ghash in dict3:
        pass
      else:
        dict3[ghash] = (fn, pos, sheaders)

    if dup:
      dups += 1
    elif near_dup:
      near_dups += 1
      f_close.write(headers2s(sheaders))
      f_close.write(headers2s(xheaders))
      f_close.write('\n')
    else:
      good += 1
  print('good: ', good)
  print('dups: ', dups)
  print('near_dups: ', near_dups)
  print('dict3: ', len(dict3))


def main():
  global f_close, f_dup
  f_close = open('dup3-close.txt', 'w')
  f_dup = open('dup3-dup.txt', 'w')

  for fn in sys.argv[1:]:
    t1 = time.time()
    munch_file(fn)
    dt = time.time() - t1
    print(fn, f'{dt:.1f}s')

  f_dup.close()
  f_close.close()

if __name__ == '__main__':
  main()
