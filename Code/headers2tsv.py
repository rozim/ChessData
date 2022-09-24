import sys
import os
import chess
import chess.pgn
from pprint import pprint
import time

# Event, Site, Date, Round, White, Black and Result.

HEADERS = [
  #'Annotator',
  'Black',
  #'BlackClock',
  'BlackElo',
  #'BlackTeam',
  #'BlackTeamCountry',
  'Date',
  'ECO',
  'Event',
  'EventCountry',
  'EventDate',
  'EventRounds',
  'EventType',
  'PlyCount',
  #'Remark',
  'Result',
  'Round',
  'Site',
  #'Source',
  #'SourceDate',
  #'SourceQuality',
  #'SourceTitle',
  #'SourceVersion',
  #'SourceVersionDate',
  'TimeControl',
  'White',
  #'WhiteClock',
  'WhiteElo',
  'WhiteTeam',
  #'WhiteTeamCountry',
  'xfile',
  'xeco',
  'xeco2'
]

NUMERIC = [
  'BlackElo',
  'WhiteElo',
  'PlyCount'
]

    # filter:
# [SetUp "1"]
# [FEN "qnrbbnkr/pppppppp/8/8/8/8/PPPPPPPP/QNRBBNKR w HChc - 0 1"]



def parse_openings(fn):
  op = {}
  op2 = {}
  eco_count = {}
  lines2 = []
  with open(fn, 'r') as f:
    for line in f.readlines():
      ar = line.split('\t')
      assert(len(ar) == 3)
      eco = ar[0]
      if eco == 'eco':  # header row
        continue
      name = ar[1]
      uci = ar[2]
      import io
      pgn = io.StringIO(uci)
      board = chess.Board()
      game = chess.pgn.read_game(pgn)
      for move in game.mainline_moves():
        board.push(move)
      sfen = board.fen().split(' ')[0]
      op[sfen] = eco
      subvar = eco_count.get(eco, 0)
      eco_count[eco] = subvar + 1
      op2[sfen] = f'{eco}.{subvar}'
      lines2.append((op2[sfen], name, uci))
  return op, op2, lines2


def sanitize(header, s):
  clean = s.replace('\t', '?')
  if header in NUMERIC:
      try:
          return str(int(clean))
      except ValueError:
          return '0'
  return clean


def munch_game(game, basename, openings, openings2):
  h = game.headers
  if 'FEN' in h or 'SetUp' in h:
    return None
  h['xfile'] = basename
  board = chess.Board()
  ply = 0
  xeco = '?'
  xeco2 = '?'
  for ply, move in enumerate(game.mainline_moves()):
    board.push(move)
    sfen = board.fen().split(' ')[0]
    xeco = openings.get(sfen, xeco)
    xeco2 = openings2.get(sfen, xeco2)
  h['xeco'] = xeco
  h['xeco2'] = xeco2
  if 'PlyCount' not in h:
    h['PlyCount'] = str(ply)
  ar = [sanitize(header, h.get(header, '')) for header in HEADERS]
  return '\t'.join(ar)


def munch_file(fn, openings, openings2):
  t1 = time.time()
  t_last_status = t1
  good = 0
  bad = 0
  base = os.path.basename(fn)
  assert base.endswith('.pgn')
  tsv = base[:-3] + 'tsv'
  out_fn = f'../Headers/{tsv}'
  #print('Out: ', out_fn)
  if os.access(out_fn, os.R_OK):
    print('Already: ', out_fn)
    return
  out = open(out_fn, 'w')

  with open(fn, 'r', encoding='utf-8', errors='replace') as f:
    fsize = f.seek(0, 2)
    print(fn, fsize)
    f.seek(0, 0)
    while True:
      g = chess.pgn.read_game(f)
      if g is None:
        break
      s = munch_game(g, base, openings, openings2)

      if s is None:
        bad += 1
        continue
      out.write(s + '\n')
      if s:
        good += 1
      else:
        bad += 1
      now = time.time()

      if now > (t_last_status + 60.0):
        pos = f.seek(0, 1)
        print('Tick', good, bad, pos, f'{100.0*(pos/fsize):.1f}%')
        t_last_status = now
  out.close()
  dt = time.time() - t1
  print(fn, ':', base, out_fn, 'good', good, 'bad', bad, f'{dt:.1f}s')


fo = open(f'../Headers/openings2.tsv', 'w')
openings = {}
openings2 = {}
for ch in ['a', 'b', 'c', 'd', 'e']:
  oc, oc2, lines2 = parse_openings(f'../../chess-openings/{ch}.tsv')
  openings.update(oc)
  openings2.update(oc2)
  for tup in lines2:
    fo.write(' '.join(tup))

print('Openings:   ', len(openings))
print('Openings/2: ', len(openings2))

for fn in sys.argv[1:]:
  try:
    munch_file(fn, openings, openings2)
  except ValueError:
    print('BAD/0', fn)
