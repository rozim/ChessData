import chess
import chess.engine
from chess import WHITE, BLACK
import time

FEN = '2rq2k1/pp3p2/1bn1b2p/1B1p2p1/3Nn3/1NP3B1/PP3PPP/3RQ1K1 w - - 8 21'
FEN = '8/5K2/1bp4p/8/2p5/2k5/PPPPPPPP/qqqqqqqq b - - 5 16'
HASH = 512
THREADS = 1 # reproducible

engine = chess.engine.SimpleEngine.popen_uci('stockfish')
engine.configure({"Hash": HASH})
engine.configure({"Threads": THREADS})

f = open('analysis-demo-log.txt', 'w')
f.write(FEN)
f.write('\n')
f.write(str(chess.Board(FEN)))
f.write('\n')
f.flush()
t0 = time.time()
t1 = time.time()
with engine.analysis(chess.Board(FEN)) as analysis:
  for info in analysis:
    f.write('INFO: ' + str(info) + '\n\n')
    f.flush()
    t2 = time.time()
    dt = t2 - t1
    dt0 = t2 - t0
    t1 = time.time()
    #print('INFO: ', info)
    if 'depth' not in info or 'pv' not in info or 'score' not in info or 'nodes' not in info or 'upperbound' in info or 'lowerbound' in info:
      f.write('[skip]\n')
      continue
    try:
      depth = int(info.get('depth'))
      score = int(info.get('score').pov(WHITE).score(mate_score=100000))
      pv = info.get('pv')
      pv = ' '.join([move.uci() for move in pv])
      nodes = int(info.get('nodes'))
    except AttributeError:
      print('BUG: ', info)

    print(f'{dt0:5.1f}s {dt:5.1f}s {depth:2d} {score:8d} {nodes:8d}   |  {pv}')
    f.write(f'LINE: {dt0:5.1f}s {dt:5.1f}s {depth:2d} {score:8d} {nodes:8d}   |  {pv}\n')

    # Arbitrary stop condition.
    if info.get('depth', 0) > 40:
      break

engine.quit()
