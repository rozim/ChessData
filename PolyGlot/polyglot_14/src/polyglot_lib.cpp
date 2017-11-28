
#include <vector>
#include <assert.h>
#include <stdlib.h>

#include "polyglot_lib.h"

#include "attack.h"
#include "fen.h"
#include "hash.h"
#include "move.h"
#include "move_do.h"
#include "move_gen.h"
#include "move_legal.h"
#include "option.h"
#include "pgn.h"
#include "piece.h"
#include "san.h"
#include "square.h"
#include "util.h"

using std::vector;


void polyglot_init() {
  util_init();
  option_init();
  square_init();
  piece_init();
  attack_init();
  hash_init();
  my_random_init();
}

void polyglot_quit() {
  fprintf(stderr, "QUIT");
  abort();
  assert(false);
  exit(100);
}
