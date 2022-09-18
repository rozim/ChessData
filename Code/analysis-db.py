import sys
import os
import json

import time
import sqlitedict

import chess
from chess import WHITE, BLACK
import chess.engine
import chess.pgn

FN = 'sinqcup22.pgn'
FEN = 'rn2kbnr/ppq2pp1/4p3/2pp2Bp/2P4P/1Q6/P2NNPP1/3RK2R w Kkq - 2 13'
MULTIPV = 50
MIN_PLY = 20
MAX_PLY = 120

MAX_DEPTH = 12
MAX_GAMES = 0

HASH = 512
THREADS = 1 # reproducable

COMMIT_FREQ = 5 # games

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


def simplify_pv(pv):
  return [move.uci() for move in pv]


def simplify_score(score, board):
  return score.pov(WHITE).score()


def simplify_multi(multi, board):
  for i, m in enumerate(multi):
    if i == 0: # nodes
      yield {'ev': simplify_score(m['score'], board),
             'pv': simplify_pv(m['pv']),
             'nodes': m['nodes']}
    else: # leave out nodes
      yield {'ev': simplify_score(m['score'], board),
             'pv': simplify_pv(m['pv'])}


def simplify_fen(board):
  #rn2kbnr/ppq2pp1/4p3/2pp2Bp/2P4P/1Q6/P2NNPP1/3RK2R w Kkq - 2 13
  return ' '.join(board.fen().split(' ')[0:4])


def main():
  ncache = 0
  nwrite = 0
  engine = chess.engine.SimpleEngine.popen_uci('stockfish')
  engine.configure({"Clear Hash": None})
  engine.configure({"Hash": HASH})
  engine.configure({"Threads": THREADS})

  db = sqlitedict.SqliteDict('analysis.sqlite',
                             encode=json.dumps, decode=json.loads)

  for gnum, game in enumerate(gen_games(FN)):
    if gnum % COMMIT_FREQ == 0:
      db.commit()
    if MAX_GAMES > 0 and gnum >= MAX_GAMES:
      break
    headers = game.headers


    t1 = time.time()
    for ply, (move, board) in enumerate(gen_moves(game)):
      if ply < MIN_PLY or ply > MAX_PLY:
        continue

      engine.configure({"Clear Hash": None})
      multi = None
      for depth in range(MAX_DEPTH + 1):
        sfen = f'{simplify_fen(board)}|{depth}'
        if sfen in db:
          ncache += 1
          continue
        multi = engine.analyse(board, chess.engine.Limit(depth=depth), multipv=MULTIPV)
        db[sfen] = list(simplify_multi(multi, board))
        nwrite += 1

      if multi:
        #print(ply, move, multi[0]['score'].pov(WHITE))
        pass
    dt = time.time() - t1
    print(f'{gnum:4d} {headers["White"]:24s} - {headers["Black"]:24s} : {headers["Result"]:7.7s} {dt:.1f}s')

  print('Cache: ', ncache)
  print('Write: ', nwrite)
  db.commit()
  db.close()
  engine.quit()

if __name__ == "__main__":
  main()
