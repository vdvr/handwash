#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <signal.h>
#include <termios.h>

#include "pkghandler.h"
#include "serial.h"

void serialize(struct Pkg* pkg, char* serialized) {
	memset(pkg->command, '\0', 64);
	memset(pkg->arguments, '\0', 64);
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
	memset(pkg->command, '\0', 64);
	memset(pkg->arguments, '\0', 64);
        if (*serialized++ == STX) {
		while (*serialized == STX)
			serialized++;
                for (int i=0; *serialized != '\r'; i++)
                        pkg->command[i] = *serialized++;
                for (int i=0; *serialized != ETX; i++) {
                        if (i > 64) return -1;
                        pkg->arguments[i] = *serialized++;
                }
                return 0;
        }
        return -1;
};
void send_pkg(int fd, char* pkg) {
        do {
                serial_send_char(fd, *pkg);
        } while(*pkg++ != 0);
};
