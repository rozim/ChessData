import pgn
import sys

n = 0
bad = 0
# Event, Site, Date, Round, White, Black and Result.

for game in pgn.loads(file(sys.argv[1]).read()):
    try:
        print("{},{},{},{},{},{},{},{},{}".format(
            game.event,
            game.site,
            game.date,
            game.round,
            game.white,
            game.black,
            game.result,
            game.whiteelo,
            game.blackelo))
    except AttributeError:
        bad += 1
        print("{}".format(game.dumps()))
    n += 1          

print("n={}".format(n))
print("bad={}".format(bad))    


