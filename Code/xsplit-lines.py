# Split on lines and aim to be close to the github limit of 50M.

import os
import sys


goal = 49 * 1024 * 1024
github_limit = 50 * 1024 * 1024

for fn in sys.argv[1:]:
  if os.stat(fn).st_size < github_limit:
    print(f'Pass, small enough: {fn}')
    continue

  chunk = -1
  out_f = None

  print(f'Read {fn}')
  with open(fn, 'r', encoding='utf-8', errors='replace') as f:
    for line in f.readlines():

      if out_f is None:
        chunk += 1
        out_fn = f'{fn}-chunk-{chunk:02d}'
        out_f = open(out_fn, 'w')
        print(f'Write {out_fn}')
        running = 0

      out_f.write(line)
      running += len(line)

      if running >= goal:
        out_f.close()
        out_f = None
