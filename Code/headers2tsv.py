import pgn
import sys

# Event, Site, Date, Round, White, Black and Result.

def sanitize(s):
    return s.replace("\t", " ")

for fn in sys.argv[1:]:
    with file(fn) as f:
        for game in pgn.loads(f.read()):
            try:
                print("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(
                    sanitize(game.event),
                    sanitize(game.site),
                    sanitize(game.date),
                    sanitize(game.round),
                    sanitize(game.white),
                    sanitize(game.black),
                    sanitize(game.result),
                    sanitize(game.whiteelo),
                    sanitize(game.blackelo)))
            except AttributeError:
                pass






