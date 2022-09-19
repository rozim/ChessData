import chess
from chess import WHITE, BLACK
import chess.engine
import chess.pgn
import time

FEN = 'rn2kbnr/ppq2pp1/4p3/2pp2Bp/2P4P/1Q6/P2NNPP1/3RK2R w Kkq - 2 13'

HASH = 512

THREADS = 12
DEPTH = 16
MULTIPV = 50

# 1, 256: 15.4s
# 1, 512: 15.5s
# 1, 128: 13.6
# ---
# iterative deepening
# multipv=3
#
# 1, 64: 20.7s
# 1, 128: 17.9s
# 1, 256: 18.0s
# 1, 512: 19.3s
#
# multipv=50 depth=16
# 1, 512: 47.3
# 1, 512: 47.5
# 1, 256: 48.3
# 1, 128: 51.7
# 1, 1024: 55.5
# 1, 2048: 53.2
# 2, 512: 42.6
# 3, 512: 39.8
# 3, 512: 40.0
# 4, 512: 39.0
# 6, 512: 35s     (vs 40+, so faster)
# 8, 512: 36s
# 12, 512: 43s (too many threads)

engine = chess.engine.SimpleEngine.popen_uci('stockfish')
# print(engine.options.keys())
engine.configure({"Clear Hash": None})
engine.configure({"Hash": HASH})
engine.configure({"Threads": THREADS})

board = chess.Board(FEN)

t1 = time.time()
for depth in range(DEPTH):
  multi = engine.analyse(board, chess.engine.Limit(depth=depth), multipv=MULTIPV)
for m in multi:
  print(m)
  print()
print(f'dt: {time.time()-t1:.1f}')

engine.quit()
