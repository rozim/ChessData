import sys
from itertools import groupby

goal = 3

chunk = 1
bytes = 40 * 1024 * 1024

with open(sys.argv[1], 'r') as f:
  ar, space = [], 0
  for line in [x.strip() for x in f]:
    if line.startswith("[Event"):
      if space >= bytes:
        print "chunk {}, lines {}, bytes {}".format(chunk, len(ar), sum([len(x) for x in ar]))
        with open("chunk_{}".format(chunk), 'w') as fw:
          fw.write('\n'.join(ar))
          chunk += 1
        ar, space = [], 0
    ar.append(line)
    space += len(line) + 1

  if len(ar) > 0:
    print "chunk {}, lines {}, bytes {}".format(chunk, len(ar), sum([len(x) for x in ar]))
    with open("chunk_{}".format(chunk), 'w') as fw:
      fw.write('\n'.join(ar))


