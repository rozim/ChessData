from absl import app
from absl import flags

import chess.pgn

FLAGS = flags.FLAGS
flags.DEFINE_string('pgn', '', '')


def main(argv):
  n = 0
  with open(FLAGS.pgn, 'r', encoding='utf-8', errors='replace') as f:
    while True:
      headers = chess.pgn.read_headers(f)
      if headers is None:
        break
      n += 1
  print(n)


if __name__ == "__main__":
  app.run(main)
