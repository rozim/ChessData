import chess
import chess.pgn
from chess import WHITE, BLACK
import chess.engine


def gen_games(fn):
  with open(fn, 'r', encoding='utf-8', errors='replace') as f:
    fsize = f.seek(0, 2) # eof
    f.seek(0, 0) # rewind
    while True:
      g = chess.pgn.read_game(f)
      if g is None:
        return
      # 2nd arg is pct
      yield g, (f.seek(0, 1) / fsize)

def gen_games_pos(fn):
  with open(fn, 'r', encoding='utf-8', errors='replace') as f:
    fsize = f.seek(0, 2) # eof
    f.seek(0, 0) # rewind
    while True:
      g = chess.pgn.read_game(f)
      if g is None:
        return
      pos = f.seek(0, 1)
      yield g, (pos / fsize), pos


def gen_moves(game):
  board = game.board()
  for ply, move in enumerate(game.mainline_moves()):
    yield move.uci(), board.san(move), ply, board
    board.push(move)


def gen_fens(game):
  board = game.board()
  for ply, move in enumerate(game.mainline_moves()):
    board.push(move)
    yield board.fen() # FEN after move


def simplify_pv(pv):
  return [move.uci() for move in pv]


def simplify_score(score, board):
  return score.pov(WHITE).score()


def simplify_multi(multi, board):
  for i, m in enumerate(multi):
    pv = m.get('pv', [])
    nodes = m.get('nodes', 0)
    if 'pv' not in m:
      continue
    assert 'score' in m, (m, 'multi=', multi, 'fen=', board.fen())

    if i == 0: # nodes
      yield {'ev': simplify_score(m['score'], board),
             'pv': simplify_pv(pv),
             'nodes': nodes}
    else: # leave out nodes
      yield {'ev': simplify_score(m['score'], board),
             'pv': simplify_pv(pv)}


def simplify_multi2(multi, board):

  def _to_san(board, pv):
    board = board.copy()
    res = []
    for move in pv:
      res.append(board.san(move))
      board.push(move)
    return ' '.join(res)

  for i, m in enumerate(multi):
    pv = m.get('pv', [])
    nodes = m.get('nodes', 0)
    if 'pv' not in m:
      continue
    assert 'score' in m, (m, 'multi=', multi, 'fen=', board.fen())

    if i == 0: # nodes
      yield {'ev': simplify_score(m['score'], board),
             'pv': simplify_pv(pv),
             'best_move': pv[0].uci(),
             'best_san': board.san(pv[0]),
             'pv_san': _to_san(board, pv),
             'nodes': nodes}
    else: # leave out nodes
      yield {'ev': simplify_score(m['score'], board),
             'best_move': pv[0].uci(),
             'best_san': board.san(pv[0]),
             'pv_san': _to_san(board, pv),
             'pv': simplify_pv(pv)}


def simplify_fen(board):
  #rn2kbnr/ppq2pp1/4p3/2pp2Bp/2P4P/1Q6/P2NNPP1/3RK2R w Kkq - 2 13
  return ' '.join(board.fen().split(' ')[0:4])


def raw_position_fen(board):
  #rn2kbnr/ppq2pp1/4p3/2pp2Bp/2P4P/1Q6/P2NNPP1/3RK2R w Kkq - 2 13
  return ' '.join(board.fen().split(' ')[0])


def sizeof(obj):
  size = sys.getsizeof(obj)
  if isinstance(obj, dict): return size + sum(map(sizeof, obj.keys())) + sum(map(sizeof, obj.values()))
  if isinstance(obj, (list, tuple, set, frozenset)): return size + sum(map(sizeof, obj))
  return size


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
