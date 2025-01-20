from absl import app
from absl import flags

import sys

import chess.pgn

FLAGS = flags.FLAGS
flags.DEFINE_string('pgn', '', '')

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
]

NUMERIC = [
  'BlackElo',
  'WhiteElo',
  'PlyCount'
]


def main(argv):
  with open(FLAGS.pgn, 'r', encoding='utf-8', errors='replace') as fp:
    while True:
      headers = chess.pgn.read_headers(fp)
      if headers is None:
        break

      fields = []
      for f in HEADERS:
        if f in NUMERIC:
          # call int to parse
          try:
            v = headers.get(f, '')
            if v == '':
              fields.append('')
            else:
              fields.append(str(v))
          except ValueError:
            sys.stderr.write('Headers: ' + str(headers) + '\n')
            sys.stderr.write('Field: ' + str(f) + '\n')
            sys.stderr.write('Value: ' + str(headers[f]) + '\n')
            break
        else:
          fields.append(headers.get(f, '').replace('\t', '?'))

      print('\t'.join(fields))



if __name__ == "__main__":
  app.run(main)
