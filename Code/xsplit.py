import os
import sys


bytes = 25 * 1024 * 1024
github_limit = 50 * 1024 * 1024

for fn in sys.argv[1:]:
  assert fn.endswith(".pgn")
  if "_part" in fn or "_chunk_" in fn:
    continue
  if os.stat(fn).st_size < github_limit:
    print("Pass, small enough: {}".format(fn))
    continue
  print("Open {}".format(fn))
  chunk = 1  
  base = fn[0:-4] # no ext
  with open(fn, 'r') as f:
    ar, space = [], 0
    prev_blank = True # 1st line in file is preceeded by a virtual blank line
    for line in (x.strip() for x in f):
      if prev_blank:
        prev_blank = False
        if space >= bytes:
          assert space < github_limit, space
          print "chunk {}, lines {}, bytes {}".format(chunk, len(ar), sum([len(x) for x in ar]))
          with open("{}_part{}.pgn".format(base, chunk), 'w') as fw:
            fw.write('\n'.join(ar))
            chunk += 1
          ar, space = [], 0
      else:
        prev_blank = (line == "")
      ar.append(line)
      space += len(line) + 1

    if len(ar) > 0:
      print "chunk {}, lines {}, bytes {}".format(chunk, len(ar), sum([len(x) for x in ar]))
      with open("{}_part{}.pgn".format(base, chunk), 'w') as fw:
        fw.write('\n'.join(ar))
    print("RM {}".format(fn))
    os.remove(fn)


