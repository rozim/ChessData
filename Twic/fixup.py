

import sys

yes = 0
no = 0
for line in sys.stdin.readlines():
  line = line.strip()
  line = line.replace('\\', '\\\\')
  nq = line.count('"')
  if nq > 2:
    pos = 0
    line2 = ""
    for ch in line:
      if ch == '"':
        if pos == 0 or pos == nq-1:
          line2 += '"'
        else:
          line2 += '\\\"'
        pos += 1
      else:
        line2 += ch
    print line2
  else:
    print line



  
