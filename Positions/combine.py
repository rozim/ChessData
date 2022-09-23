

last_fen = None
last_count = None
with open('tmp2.csv', 'r') as f:
  for line in f.readlines():
    line = line.strip()
    ar = line.split(',')
    assert len(ar) == 2
    fen, count = ar
    count = int(count)
    if fen == last_fen:
      last_count += count
    else:
      if last_fen != None:
        print(f'{last_fen},{last_count}')
      last_fen = fen
      last_count = count

if last_fen != None:
  print(f'{last_fen},{last_count}')
