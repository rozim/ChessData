
#include "move.h"
#include "move_do.h"
#include "pgn.h"
#include "san.h"
#include "square.h"
#include "util.h"
#include "move_legal.h"
#include "move_gen.h"
#include "polyglot_lib.h"


// Read in a game and show all legal moves.

int main(int argc, char * argv[]) {
  polyglot_init();
  while (*++argv) {
    printf("%s\n", *argv);
    pgn_t pgn[1];
    pgn_open(pgn, *argv);
    while (pgn_next_game(pgn)) {
      board_t board[1];      
      board_start(board);
      char str[256];
      while (pgn_next_move(pgn, str, 256)) {
        int move = move_from_san(str, board);
        if (move == MoveNone || !move_is_legal(move, board)) {
          printf("illegal move \"%s\" at line %d, column %d\n",
                   str, pgn->move_line, pgn->move_column);	  
	  break;
        }
	printf("%s\n", str);
        move_do(board, move); // tbd: how to undo? board_copy?
	list_t list[1];
	gen_legal_moves(list,board); // gen_moves() not as interesting
	for (int i = 0; i < list_size(list); i++) {
	  int move = list_move(list,i);
	  char move_string[256];
	  if (!move_to_san(move, board, move_string, 256)) ASSERT(false);
	  printf("\t%d. %s\n", i, move_string);
	}
      }
    }
    pgn_close(pgn);
  }
}
