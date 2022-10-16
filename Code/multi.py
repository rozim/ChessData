import chess.engine
import chess
import time

FEN = '2k4r/4np2/p1p5/8/4B3/1P2P3/P4P2/1K1R4 b - -'

engine = chess.engine.SimpleEngine.popen_uci('./stockfish')
engine.configure({"Clear Hash": 1})
engine.configure({"Hash": 256})
engine.configure({"Threads": 1})

board = chess.Board(FEN)
print(board)
for d in range(31):
  t1 = time.time()
  res = engine.analyse(board, chess.engine.Limit(depth=d))
  dt = time.time() - t1
  print(d, f'{dt:.1f}s', res['score'].white(), res['nodes'], [m.uci() for m in res['pv']])
  print()
        #print([m.uci() for m in ent['pv']])
        #print()
engine.quit()
