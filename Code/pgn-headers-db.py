import sys
import chess
import chess.pgn

from absl import app
from absl import flags

FLAGS = flags.FLAGS
flags.DEFINE_string('pgn', None, 'Input')
flags.mark_flag_as_required('pgn')

# FN = 'sinqcup22.pgn'

def gen_games(fn):
  f = open(fn, 'r', encoding='utf-8', errors='replace')
  while True:
    g = chess.pgn.read_game(f)
    if g is None:
      return
    yield g

def gen_headers(fn):
  for g in gen_games(fn):
    yield g.headers


def main(_argv):
  del _argv
  headers = set()

  for h in gen_headers(FLAGS.pgn):
    #print(h.get('Variation', '|'), ':', h.get('Event', '|'), ':', h.get('EventType', '|'))
    headers.update(h.keys())
  print()
  for h in sorted(headers):
    print(h)


if __name__ == "__main__":
  app.run(main)
