msgWriter : msgWriter.o helper.o tap.o
	gcc -o msgWriter msgWriter.o helper.o tap.o

msgWriter.o : msgWriter.c msg.h helper.h pkgstruct.h tap.h
	gcc -c msgWriter.c

helper.o : helper.c msg.h helper.h pkgstruct.h
	gcc -g -c helper.c

msgReader : msgReader.o helper.o
	gcc -o msgReader msgReader.o helper.o

msgReader.o : msgReader.c msg.h helper.h pkgstruct.h
	gcc -g -c msgReader.c

worker : worker.o pkg.o helper.o
	gcc -o worker worker.o pkg.o helper.o -lwiringPi

pkg.o : pkg.c pkgstruct.h 
	gcc -g -c pkg.c

worker.o : worker.c pkg.h pkgstruct.h msg.h 
	gcc -g -c worker.c

tap.o: tap.c helper.h
	gcc -g -c tap.c

clean:
	rm *.o msgWriter msgReader worker

all : 
	make worker
	make msgReader
	make msgWriter

rebuild:
	make clean
	make all