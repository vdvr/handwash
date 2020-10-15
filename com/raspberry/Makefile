msgWriter: msgWriter.o helper.o
	gcc -o msgWriter msgWriter.o helper.o

msgWriter.o: msgWriter.c msg.h helper.h pkghandler.h
	gcc -c msgWriter.c

helper.o: helper.c msg.h helper.h pkghandler.h
	gcc -g -c helper.c

msgReader: msgReader.o helper.o
	gcc -o msgReader msgReader.o helper.o

msgReader.o: msgReader.c msg.h helper.h pkg.h
	gcc -g -c msgReader.c

worker: worker.o pkghandler.o helper.o
	gcc -o worker worker.o pkghandler.o helper.o -lpigpio -lrt

pkghandler.o: pkghandler.c pkg.h 
	gcc -g -c pkghandler.c

worker.o: worker.c pkghandler.h pkg.h msg.h 
	gcc -g -c worker.c

clean:
	rm *.o msgWriter msgReader worker

all: 
	make worker
	make msgReader
	make msgWriter

rebuild:
	make clean
	make all