import chess
import chess.engine
import time
import logging

HASH = 512
THREADS = 1 # reproducible
MULTIPV = 1
DEPTH = 16
FEN = 'rb1q1n1k/4r1p1/1pp1pN1p/p2pP3/3P2RN/P2Q4/1PP2P1P/6RK b - - 0 1'

def open_engine():
  engine = chess.engine.SimpleEngine.popen_uci('./stockfish')
  engine.configure({"Hash": HASH})
  engine.configure({"Threads": THREADS})
  return engine

print(FEN)
print(chess.Board(FEN))
print()
logging.basicConfig(level=logging.DEBUG)
logging.getLogger().setLevel(logging.DEBUG)
for depth in [16]:
  board = chess.Board(FEN)
  engine = open_engine()
  t1 = time.time()
  multi = engine.analyse(board, chess.engine.Limit(depth=depth), multipv=MULTIPV)
  dt = time.time() - t1
  print(depth, multi[0]['nodes'], f'{dt:.1f}s')
  engine.quit()
