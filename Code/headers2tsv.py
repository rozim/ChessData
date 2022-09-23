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
      op[board.fen().split(' ')[0]] = eco
  return op


def sanitize(header, s):
  clean = s.replace('\t', '?')
  if header in NUMERIC:
      try:
          return str(int(clean))
      except ValueError:
          return '0'
  return clean


def munch_game(game, basename, openings):
  h = game.headers
  if 'FEN' in h or 'SetUp' in h:
    return None
  h['xfile'] = basename
  board = chess.Board()
  ply = 0
  xeco = '?'
  for ply, move in enumerate(game.mainline_moves()):
    board.push(move)
    fen = board.fen().split(' ')[0]
    xeco = openings.get(fen, xeco)
  h['xeco'] = xeco
  if 'PlyCount' not in h:
    h['PlyCount'] = str(ply)
  ar = [sanitize(header, h.get(header, '')) for header in HEADERS]
  return '\t'.join(ar)


def munch_file(fn, openings):
  t1 = time.time()
  good = 0
  bad = 0
  base = os.path.basename(fn)
  assert base.endswith('.pgn')
  tsv = base[:-3] + 'tsv'
  out_fn = f'../Headers/{tsv}'
  #print('Out: ', out_fn)
  out = open(out_fn, 'w')
  with open(fn, 'r', encoding='utf-8', errors='replace') as f:
    while True:
      g = chess.pgn.read_game(f)
      if g is None:
        break
      s = munch_game(g, base, openings)
      out.write(s + '\n')
      if s:
        good += 1
      else:
        bad += 1
  out.close()
  dt = time.time() - t1
  print(fn, ':', base, out_fn, 'good', good, 'bad', bad, f'{dt:.1f}s')


openings = {}
for ch in ['a', 'b', 'c', 'd', 'e']:
  openings.update(parse_openings(f'../../chess-openings/{ch}.tsv'))

print('Openings: ', len(openings))

for fn in sys.argv[1:]:
  munch_file(fn, openings)
