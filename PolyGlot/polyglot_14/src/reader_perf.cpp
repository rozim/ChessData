
#include <sys/time.h>
#include <time.h>

#include "board.h"
#include "move.h"
#include "move_do.h"
#include "pgn.h"
#include "san.h"
#include "square.h"
#include "util.h"
#include "move_legal.h"
#include "polyglot_lib.h"



// Test parser

int main(int argc, char * argv[]) {
  polyglot_init();
  long tot_games = 0;
  time_t t0 = time(0L);
  while (*++argv) {
    time_t t1 = time(0L);
    int games = 0;
    printf("%s\n", *argv);
    pgn_t pgn[1];
    pgn_open(pgn, *argv);
    while (pgn_next_game(pgn)) {
      board_t board[1];      
      board_start(board);
      char str[256];
      while (pgn_next_move(pgn,str,256)) {
        int move = move_from_san(str,board);
        if (move == MoveNone || !move_is_legal(move,board)) {
          printf("illegal move \"%s\" at line %d, column %d\n",
                   str, pgn->move_line,pgn->move_column);	  
	  break;
        }
        move_do(board,move);
      }
      games++;
    }
    pgn_close(pgn);
    time_t t2 = time(0L);
    time_t dt = t2 - t1;
    long rate = (games + (dt/2))/ (dt == 0 ? 1 : dt);
    printf("%s games=%d time=%ld (s) rate=%ld (gps)\n", *argv, games, dt, rate);
    tot_games += games;
  }
  time_t tot_time = time(0L) - t0;
  long tot_rate = (tot_games + (tot_time / 2)) / (tot_time == 0 ? 1 : tot_time);
  printf("Total     : %ld\n", tot_games);
  printf("Total time: %ld\n", tot_time);
  printf("Final rate: %ld\n", tot_rate);


}
