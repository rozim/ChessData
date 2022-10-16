import logging
import sys
import os
import json
import random

import time
import sqlitedict

from absl import app
from absl import flags

FLAGS = flags.FLAGS

def to_int(foo):
  return int(foo)

def main(argv):
  assert len(argv) == 2
  db = sqlitedict.open(filename=argv[1],
                       flag='c',
                       encode=json.dumps,
                       decode=json.loads)

  print('sfen\tdepth\tev\tmate\tnodes\tbest\tpv')
  for key, v in db.items():
    if len(v) == 0: # argh, mate
      print(key)
      assert False
      continue
    assert len(v) == 1, (n, v)

    try:
      sfen, depth = key.split('|')
      depth = to_int(depth)
      multi = v[0]
      ev = to_int(multi['ev'])
      pv = multi['pv']
      mate = multi['mate']
      nodes = to_int(multi['nodes'])
      best = pv[0]
      print(f'{sfen}\t{depth}\t{ev}\t{mate}\t{nodes}\t{best}\t{pv}')
    except TypeError:
      print('BUG: ', key)
      assert False




if __name__ == "__main__":
  app.run(main)
