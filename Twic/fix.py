
# get rid of comment lines with two dashes
# that TWIC sometimes has

import sys, os

def doit(fin, fout):
  ar = [line for line in fin.readlines()]
  rm = 0
  for i in range(len(ar) - 1):
    if ar[i + 1].startswith('--'):
      rm += 1
      ar[i] = ar[i + 1] = None
      i += 1
  for line in (ent for ent in ar if ent is not None):
    fout.write(line)
  return  rm


for fn in sys.argv[1:]:
  rm = doit(open(fn, 'r', encoding='utf-8', errors='replace'),
            open('fix-' + fn, 'w'))
  print(fn, rm)
