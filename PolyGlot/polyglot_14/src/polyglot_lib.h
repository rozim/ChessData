#if !defined(POLYGLOT_LIB_H_INCLUDED)
#define POLYGLOT_LIB_H_INCLUDED


#include "attack.h"
#include "board.h"
#include "colour.h"
#include "epd.h"
#include "fen.h"
#include "game.h"
#include "move.h"
#include "move_do.h"
#include "move_gen.h"
#include "move_legal.h"
#include "pgn.h"
#include "piece.h"
#include "san.h"
#include "search.h"
#include "square.h"

// dss: init everything
extern void polyglot_init();
extern void polyglot_quit();

#endif
