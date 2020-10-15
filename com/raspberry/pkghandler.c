#include <pigpio.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include "pkghandler.h"

#define STX 2
#define ETX 3

void serialize(struct Pkg pkg, char* serialized) {
        *serialized++ = STX;
        *serialized++ = pkg.command_length;
        for (int i = 0; i<=pkg.command_length; i++)
                *serialized++ = pkg.command[i];
        *serialized++ = pkg.arguments_length;
        for (int i = 0; i<=pkg.arguments_length; i++)
                *serialized++ = pkg.arguments[i];
        *serialized++ = ETX;
        *serialized++ = 0;
};
int deserialize(char* serialized, struct Pkg *pkg) {
        if (*serialized++==STX) {
                int i = 0;
                int t = 0;
                int length = atoi(*serialized++);
                int command_length = length;
                char command[command_length];
                for (int i=0; i<=command_length; i++)
                        command[i] = *serialized++;
                i = 0;
                length = atoi(*serialized++);
                int arguments_length = length;
                char arguments[arguments_length];
                for (int i=0; i<=arguments_length; i++)
                        arguments[i] = *serialized++;
                length = atoi(*serialized++);
                if (length == 3)
                        return 0;
                else
                        return -1;
        } else return -1;
};
void send_pkg(int fd, char* pkg) {
        do {
                serWriteByte(fd, *pkg);
        } while(*pkg++ != 0);
};