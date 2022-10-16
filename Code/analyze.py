import sys
import chess
from chess import WHITE, BLACK
import chess.engine
import chess.pgn
import time
from util import *

FEN = 'rn2kbnr/ppq2pp1/4p3/2pp2Bp/2P4P/1Q6/P2NNPP1/3RK2R w Kkq - 2 13'
FEN = '6B1/8/7p/bP1p4/2pkp2P/8/2K5/8 w - - 0 1'
#FEN = '8/6bk/8/p5p1/P5N1/4P1PP/7K/8 b - - 0 54'
#FEN = '3r4/1p3kp1/1p2r3/2p4p/2N1p3/P5PP/1PP1R1K1/8 w - - 2 38'
#FEN = 'r1b2rk1/1p2qpp1/1ppp1n1p/8/2B1PR2/P2P3P/1PP3PN/R2Q2K1 w - - 0 16'
#FEN = '8/1p3kp1/1p2r3/2p4p/4p3/PP2N1PP/2P1R1K1/r7 w - - 1 42'
HASH = 512

THREADS = 1
MULTIPV = 50

engine = chess.engine.SimpleEngine.popen_uci('./stockfish')
engine.configure({'Clear Hash': None})
engine.configure({'Hash': HASH})
engine.configure({'Threads': THREADS})

board = chess.Board(FEN)

print(FEN)
t0 = time.time()
for d in range(0, 30):
  engine.configure({'Clear Hash': None})
  t1 = time.time()
  multi = engine.analyse(board, chess.engine.Limit(depth=d), multipv=1)
  dt = time.time() - t1
  m = multi[0]
  print(d, f'{dt:.1f}', m['nodes'], ':', m['score'].pov(WHITE), ':', [mv.uci() for mv in m['pv']])
  print()
  print('#simplify', d, f'{dt:.1f}s')
  print('x1: ', m['score'])
  print('x2: ', m['score'].pov(WHITE))
  print('x3: ', m['score'].pov(WHITE).score())
  print('x4: ', m['score'].pov(WHITE).score(mate_score=10000))
  print('x5: ', m['score'].pov(WHITE).score(mate_score=100000))
  print(list(simplify_multi(multi, board)))
print()
dt = time.time() - t0
print(f'{dt:.1f}s')
engine.quit()
