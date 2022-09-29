import chess
import chess.pgn
from chess import WHITE, BLACK
import chess.engine


def gen_games(fn):
  f = open(fn, 'r', encoding='utf-8', errors='replace')
  while True:
    g = chess.pgn.read_game(f)
    if g is None:
      return
    yield g


def gen_moves(game):
  board = game.board()
  for ply, move in enumerate(game.mainline_moves()):
    yield move.uci(), board.san(move), ply, board
    board.push(move)


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
