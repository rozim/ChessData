
// engine.h

#ifndef ENGINE_H
#define ENGINE_H

// includes

#include "io.h"
#include "util.h"

// types

struct engine_t {
   io_t io[1];
};

// variables

extern engine_t Engine[1];

// functions

extern bool engine_is_ok      (const engine_t * engine);

extern void engine_open       (engine_t * engine);
extern void engine_close      (engine_t * engine);

extern void engine_get        (engine_t * engine, char string[], int size);

extern void engine_send       (engine_t * engine, const char format[], ...);
extern void engine_send_queue (engine_t * engine, const char format[], ...);

#endif // !defined ENGINE_H

// end of engine.h

