msgWriter: msgWriter.o helper.o
	gcc -Wall -Wextra -o msgWriter msgWriter.o helper.o

msgWriter.o: msgWriter.c msg.h helper.h pkghandler.h
	gcc -c -Wall -Wextra msgWriter.c

helper.o: helper.c msg.h helper.h pkghandler.h
	gcc -g -Wall -Wextra -c helper.c

msgReader: msgReader.o helper.o
	gcc -Wall -Wextra -o msgReader msgReader.o helper.o

msgReader.o: msgReader.c msg.h helper.h pkg.h
	gcc -g -Wall -Wextra -c msgReader.c

worker: worker.o pkghandler.o helper.o serial.o
	gcc -Werror -Wall -Wextra -o worker worker.o serial.o pkghandler.o helper.o

serial.o: serial.h
	gcc -g -Wall -Wextra -c serial.c

pkghandler.o: pkghandler.c pkg.h serial.o
	gcc -g -Wall -Wextra -c pkghandler.c

worker.o: worker.c pkghandler.h pkg.h msg.h serial.h
	gcc -g -Wall -Wextra -c worker.c

clean:
	rm *.o msgWriter msgReader worker

all:
	make worker
	make msgReader
	make msgWriter

rebuild:
	make clean
	make all
