#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include  <signal.h>
#include  <setjmp.h>

#include "pkghandler.h"

void serialize(struct Pkg* pkg, char* serialized) {
	*serialized++ = STX;
	for(char i=0; i <= 3; i++) {
		*serialized++ = *(pkg->command+i);
	}
	*serialized++ = '\r';
	for(char i = 0; i <= 3; i++) {
		*serialized++ = *(pkg->arguments+i);
	}
	*serialized++ = ETX;
	*serialized++ = '\0';
};

int deserialize(char* serialized, struct Pkg *pkg) {
	if (*serialized++ == STX) {
		pkg = (struct Pkg*) malloc(sizeof(struct Pkg));
		for (int i=0; i <= 4; i++)
			pkg->command[i] = *serialized++;
		if (*serialized++ != '\r')
			return -1;
		for (int i=0; i <= 4; i++)
			pkg->arguments[i] = *serialized++;
		if (*serialized == ETX) {
			return 0;
		}
	}
	return -1;
};
void send_pkg(int fd, char* pkg) {
	do {
		serialPutchar(fd, *pkg);
	} while(*pkg++ != 0);
};
