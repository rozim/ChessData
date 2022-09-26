
import sys
import chess
from chess import WHITE, BLACK
import chess.engine
import chess.pgn
import time
import random

from absl import app
from absl import flags

FLAGS = flags.FLAGS
flags.DEFINE_integer('depth', 1, 'Fixed depth')
flags.DEFINE_bool('second', True, '')
flags.DEFINE_integer('close', 50, 'Threshold to be equi-optimal')
flags.DEFINE_integer('num_matches', 50, 'Number of two game matches to play')

HASH = 512
THREADS = 1

engine1 = chess.engine.SimpleEngine.popen_uci('stockfish')
engine2 = chess.engine.SimpleEngine.popen_uci('stockfish')

engine1.configure({'Hash': HASH})
engine2.configure({'Hash': HASH})
engine1.configure({'Threads': THREADS})
engine2.configure({'Threads': THREADS})


def play_best1(engine, board):
  return engine.analyse(board, chess.engine.Limit(depth=FLAGS.depth)), 0


def play_best2(engine, board):
  multi = engine.analyse(board, chess.engine.Limit(depth=FLAGS.depth), multipv=2)
  assert len(multi) == 2
  if multi[0]['score'].white().is_mate():
    return multi[0], 0
  m0 = multi[0]
  m1 = multi[1]
  s0 = m0['score'].white().score(mate_score=10000)
  s1 = m1['score'].white().score(mate_score=10000)
  if abs(s0 - s1) < FLAGS.close:
    return m1, 1 # 1=special
  else:
    return m0, 0


def gen_games(fn):
  with open(fn, 'r', encoding='utf-8', errors='replace') as f:
    while True:
      game = chess.pgn.read_game(f)
      if game is None:
        return
      yield game


def play_game(board, white_engine, black_engine, white_play, black_play, flog):
  ply = -1
  num_special = 0
  while True:
    ply += 1
    outcome = board.outcome()
    if outcome is not None:
      break

    if board.turn == WHITE:
      engine = white_engine
      play = white_play
      which = 0
    else:
      engine = black_engine
      play = black_play
      which = 1

    legal = list(board.legal_moves)
    nlegal = len(legal)
    if nlegal == 0:
      assert False, 'no legal'
      break

    dt = 0.0
    if len(legal) == 1:
      move = legal[0]
      score = 0
      nodes = 0
      flog.write(f'{ply:3d} {which:1d} {board.san(move):8s} {move.uci():6s}, {" ":6s}, {" ":8s}, {board.fen()} FORCED\n')
    else:
      t1 = time.time()
      res, special = play(engine, board)
      num_special += special
      dt = time.time() - t1
      move = res['pv'][0]
      score = int(res['score'].white().score(mate_score=10000))
      nodes = int(res['nodes'])
      star = [' ', '*'][special]
      flog.write(f'{ply:3d} {which:1d} {board.san(move):8s} {move.uci():6s}, {score:6d}, {nodes:8d}, {board.fen()} {star}\n')
    board.push(move)
  flog.flush()
  return outcome, board, num_special


def playthrough(game):
  board = chess.Board()
  for move in game.mainline_moves():
    board.push(move)
  return board


def read_opening():
  return [playthrough(game) for game in gen_games('../Openings/merged.pgn')]


def main(_argv):
  t0 = time.time()
  print(f'Depth:    {FLAGS.depth}')
  print(f'Second:   {FLAGS.second}')
  print(f'Close:    {FLAGS.close}')
  print(f'Matches:  {FLAGS.num_matches}')
  print()
  e1_win, e1_lose, e1_draw = 0, 0, 0

  opening_boards = read_opening()
  print('Openings: ', len(opening_boards))
  random.shuffle(opening_boards)

  engines = [engine1, engine2]
  if FLAGS.second:
    plays = [play_best1, play_best2]
  else:
    plays = [play_best1, play_best1]
  wwin = ['1-0', '0-1']

  flog = open('log.txt', 'w')
  tot_special = 0
  for bnum, opening_board in enumerate(opening_boards):
    if FLAGS.num_matches and bnum >= FLAGS.num_matches:
      break
    print(f'Game {bnum:4d} {opening_board.fen()}')

    for wflip in [0, 1]:
      bflip = 1 - wflip
      t1 = time.time()
      outcome, board, num_special = play_game(opening_board.copy(),
                                              engines[wflip],
                                              engines[bflip],
                                              plays[wflip],
                                              plays[bflip],
                                              flog)
      tot_special += num_special
      dt = time.time() - t1

      result = outcome.result()
      if result == wwin[wflip]:
        e1_win += 1
      elif result == wwin[bflip]:
        e1_lose += 1
      else:
        e1_draw += 1
      print(f'Game {bnum:4d}.{wflip:1d} over: {result:8s} #2: {num_special:3d} {dt:4.1f}s | win:{e1_win:3d} lose:{e1_lose:3d} draw:{e1_draw:3d} | {board.fen()}')

  flog.close()

  def _pc(a, b):
    return 100.0 * ((a + 0.0) / (b + 0.0))

  ng = e1_win + e1_lose + e1_draw
  print()
  print(f'Elapsed:  {time.time() - t0:.1f}s')
  print(f'Games:    {ng}')
  print()


  print(f'Win :     {e1_win:3d} {_pc(e1_win, ng):.1f}%')
  print(f'Lose:     {e1_lose:3d} {_pc(e1_lose, ng):.1f}%')
  print(f'Draw:     {e1_draw:3d} {_pc(e1_draw, ng):.1f}%')
  print()
  print(f'Special:  {tot_special}')
  print()
  engine1.quit()
  engine2.quit()
  print('finis')



if __name__ == "__main__":
  app.run(main)
