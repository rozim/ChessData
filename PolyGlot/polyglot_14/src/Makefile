
# files

EXE = polyglot

OBJS = adapter.o attack.o board.o book.o book_make.o book_merge.o colour.o \
       engine.o epd.o fen.o game.o hash.o io.o line.o list.o main.o move.o \
       move_do.o move_gen.o move_legal.o option.o parse.o pgn.o piece.o \
       posix.o random.o san.o search.o square.o uci.o util.o

MOST_OBJS = adapter.o attack.o board.o book.o book_make.o book_merge.o colour.o \
       engine.o epd.o fen.o game.o hash.o io.o line.o list.o move.o \
       move_do.o move_gen.o move_legal.o option.o parse.o pgn.o piece.o \
       posix.o random.o san.o search.o square.o uci.o util.o polyglot_lib.o

# rules

all: $(EXE) .depend

clean:
	$(RM) *.o .depend *.a *.so *~ move_list_demo

# general

CXX       = g++
CXXFLAGS  = -O3
LDFLAGS   = -lm

# C++

CXXFLAGS += -fno-exceptions -fno-rtti

# optimisation

CXXFLAGS += -O3
CXXFLAGS += -fomit-frame-pointer

# strip

LDFLAGS  += 

# dependencies

all : $(EXE) polyglot.a reader_perf move_list_demo reader_perf 

$(EXE): $(OBJS)
	$(CXX) $(LDFLAGS) -o $@ $(OBJS)

polyglot.so: ${MOST_OBJS}
	g++ -shared ${MOST_OBJS} -o ${@}

polyglot.a: ${MOST_OBJS}
	rm -f ${@}
	ar q ${@} ${MOST_OBJS}

reader_perf : reader_perf.o polyglot.a
	$(CXX) $(LDFLAGS) -o $@ reader_perf.o polyglot.a

move_list_demo : move_list_demo.o polyglot.a
	$(CXX) $(LDFLAGS) -o $@ move_list_demo.o polyglot.a

%.s: %.cpp
	$(CXX) -S $(CXXFLAGS) $<

.depend:
	$(CXX) -MM $(OBJS:.o=.cpp) > $@

include .depend

