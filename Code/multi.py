import chess.engine
import chess

engine = chess.engine.SimpleEngine.popen_uci('stockfish')
engine.configure({"Clear Hash": 1})
engine.configure({"Hash": 256})
engine.configure({"Threads": 1})

board = chess.Board('r4rk1/pp2bpp1/1qn1bn1p/3p4/Q6B/2NBPN2/PP1R1PPP/4K2R b K - 0 1')
for ent in engine.analyse(board, chess.engine.Limit(depth=1), multipv=3):
  print([m.uci() for m in ent['pv']])
  print()
engine.quit()
