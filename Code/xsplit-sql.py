import os
import sys


THRESHOLD = 45 * 1024 * 1024


def make_out_fn(fn, chunk):
  return fn + '-split-' + str(chunk)


def munch_file(fn, f):
  chunk = 0
  total = 0
  out_fn = make_out_fn(fn, chunk)
  print(out_fn)

  fw = open(out_fn, 'w')
  for line in f.readlines():
    fw.write(line)
    total += len(line)
    if total >= THRESHOLD:
      fw.close()
      total = 0
      chunk += 1
      out_fn = make_out_fn(fn, chunk)
      print(out_fn)
      fw = open(out_fn, 'w')
  fw.close()

for fn in sys.argv[1:]:
  print("Open {}".format(fn))
  with open(fn, 'r') as f:
    munch_file(fn, f)
