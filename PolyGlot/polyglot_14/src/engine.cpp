
// engine.cpp

// includes

#include <cerrno>
#include <cstdarg>
#include <cstdio>
#include <cstdlib>
#include <cstring>

#include <sys/types.h>
#include <unistd.h>

#include "engine.h"
#include "io.h"
#include "option.h"
#include "util.h"

// constants

static const bool UseNice = false;

static const int StringSize = 4096;

// variables

engine_t Engine[1];

// prototypes

static void my_close (int fd);
static void my_dup2  (int old_fd, int new_fd);

// functions

// engine_is_ok()

bool engine_is_ok(const engine_t * engine) {

   if (engine == NULL) return false;

   if (!io_is_ok(engine->io)) return false;

   return true;
}

// engine_open()

void engine_open(engine_t * engine) {

   const char * dir, * command;
   char string[StringSize];
   int argc;
   char * ptr;
   char * argv[256];
   int from_engine[2], to_engine[2];
   pid_t pid;

   ASSERT(engine!=NULL);

   // init

   dir = option_get_string("EngineDir");
   my_log("POLYGLOT Dir \"%s\"\n",dir);

   command = option_get_string("EngineCommand");
   my_log("POLYGLOT Command \"%s\"\n",command);

   // parse the command line and create the argument list

   if (strlen(command) >= StringSize) my_fatal("engine_open(): buffer overflow\n");
   strcpy(string,command);

   argc = 0;

   for (ptr = strtok(string," "); ptr != NULL; ptr = strtok(NULL," ")) {
      argv[argc++] = ptr;
   }

   argv[argc] = NULL;

   // create the pipes

   if (pipe(from_engine) == -1) {
      my_fatal("engine_open(): pipe(): %s\n",strerror(errno));
   }

   if (pipe(to_engine) == -1) {
      my_fatal("engine_open(): pipe(): %s\n",strerror(errno));
   }

   // create the child process

   pid = fork();

   if (pid == -1) {

      my_fatal("engine_open(): fork(): %s\n",strerror(errno));

   } else if (pid == 0) {

      // child = engine

      // close unused pipe descriptors to avoid deadlocks

      my_close(from_engine[0]);
      my_close(to_engine[1]);

      // attach the pipe to standard input

      my_dup2(to_engine[0],STDIN_FILENO);
      my_close(to_engine[0]);

      // attach the pipe to standard output

      my_dup2(from_engine[1],STDOUT_FILENO);
      my_close(from_engine[1]);

      // attach standard error to standard output

      my_dup2(STDOUT_FILENO,STDERR_FILENO);

      // set a low priority

      if (UseNice) nice(+20);

      // change the current directory

      if (dir[0] != '\0' && chdir(dir) == -1) {
         my_fatal("engine_open(): chdir(): %s\n",strerror(errno));
      }

      // launch the new executable file

      execvp(argv[0],&argv[0]);

      // execvp() only returns when an error has occured

      my_fatal("engine_open(): execvp(): %s\n",strerror(errno));

   } else { // pid > 0

      ASSERT(pid>0);

      // parent = PolyGlot

      // close unused pipe descriptors to avoid deadlocks

      my_close(from_engine[1]);
      my_close(to_engine[0]);

      // fill in the engine struct

      engine->io->in_fd = from_engine[0];
      engine->io->out_fd = to_engine[1];
      engine->io->name = "ENGINE";

      io_init(engine->io);
   }
}

// engine_close()

void engine_close(engine_t * engine) {

   ASSERT(engine_is_ok(engine));

   io_close(engine->io);
}

// engine_get()

void engine_get(engine_t * engine, char string[], int size) {

   ASSERT(engine_is_ok(engine));
   ASSERT(string!=NULL);
   ASSERT(size>=256);

   while (!io_line_ready(engine->io)) {
      io_get_update(engine->io);
   }

   if (!io_get_line(engine->io,string,size)) { // EOF
      exit(EXIT_SUCCESS);
   }
}

// engine_send()

void engine_send(engine_t * engine, const char format[], ...) {

   va_list arg_list;
   char string[StringSize];

   ASSERT(engine_is_ok(engine));
   ASSERT(format!=NULL);

   // format

   va_start(arg_list,format);
   vsprintf(string,format,arg_list);
   va_end(arg_list);

   // send

   io_send(engine->io,"%s",string);
}

// engine_send_queue()

void engine_send_queue(engine_t * engine, const char format[], ...) {

   va_list arg_list;
   char string[StringSize];

   ASSERT(engine_is_ok(engine));
   ASSERT(format!=NULL);

   // format

   va_start(arg_list,format);
   vsprintf(string,format,arg_list);
   va_end(arg_list);

   // send

   io_send_queue(engine->io,"%s",string);
}

// my_close()

static void my_close(int fd) {

   ASSERT(fd>=0);

   if (close(fd) == -1) my_fatal("my_close(): close(): %s\n",strerror(errno));
}

// my_dup2()

static void my_dup2(int old_fd, int new_fd) {

   ASSERT(old_fd>=0);
   ASSERT(new_fd>=0);

   if (dup2(old_fd,new_fd) == -1) my_fatal("my_dup2(): dup2(): %s\n",strerror(errno));
}

// end of engine.cpp

