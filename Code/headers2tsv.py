import sys
import os
import chess
import chess.pgn

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
]

NUMERIC = [
  'BlackElo',
  'WhiteElo',
  'PlyCount'
]

    # filter:
# [SetUp "1"]
# [FEN "qnrbbnkr/pppppppp/8/8/8/8/PPPPPPPP/QNRBBNKR w HChc - 0 1"]


def sanitize(header, s):
  clean = s.replace('\t', '?')
  if header in NUMERIC:
      try:
          return str(int(clean))
      except ValueError:
          return '0'
  return clean


def munch_game(g, basename):
  h = g.headers
  if 'FEN' in h or 'SetUp' in h:
    return None
  h['xfile'] = basename
  ar = [sanitize(header, h.get(header, '')) for header in HEADERS]
  return '\t'.join(ar)


def munch_file(fn):
  good = 0
  bad = 0
  base = os.path.basename(fn)
  assert base.endswith('.pgn')
  tsv = base[:-3] + 'tsv'
  out_fn = f'../Headers/{tsv}'
  print('Out: ', out_fn)
  out = open(out_fn, 'w')
  with open(fn, 'r', encoding='utf-8', errors='replace') as f:
    while True:
      g = chess.pgn.read_game(f)
      if g is None:
        break
      s = munch_game(g, base)
      out.write(s + '\n')
      if s:
        good += 1
      else:
        bad += 1
  out.close()
  print(fn, ':', base, 'good', good, 'bad', bad)



for fn in sys.argv[1:]:
  munch_file(fn)
