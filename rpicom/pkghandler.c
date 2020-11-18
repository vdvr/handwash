#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <signal.h>
#include <termios.h>

#include "pkghandler.h"
#include "serial.h"

void serialize(struct Pkg* pkg, char* serialized) {
	
	/* Zero out the command and arguments field */
	memset(pkg->command, '\0', 64);
	memset(pkg->arguments, '\0', 64);

	/* Create cursor pointers for both the pkg->command and 
	 * pkg->arguments */
	const char* _command = pkg->command;
	const char* _arguments = pkg->arguments;

	/* First we make sure the serialized string starts with an STX
	 * [ STX , _ ] 
	 * where _ is the location pointed to by serialized */
        *serialized++ = STX;

	/* Then we copy the command into serialized */
	int i = 0;
        for(; *_command != '\0';)
                *serialized++ = *_command++;

	/* Add the sepator */
        *serialized++ = SEP;

	/* Copy the arguments into serialized */
        for(; *_arguments != '\0';)
                *serialized++ = *_arguments;

	/* End serialized */
        *serialized++ = ETX;
        *serialized++ = '\0';

	/* Free up the cursor pointers and pkg */
	free((char*) _command);
	free((char*) _arguments);
	free(pkg);
};

int deserialize(char* serialized, struct Pkg *pkg) {

	/* Zero out the command and arguments field */
	memset(pkg->command, '\0', 64);
	memset(pkg->arguments, '\0', 64);
	
	/* Create cursor pointers for both the pkg->command and 
	 * pkg->arguments */
	char* _command = pkg->command;
	char* _arguments = pkg->arguments;

	/* Does the serialized string start with STX? */
	if (*serialized++ != STX)
		return 1;

	/* Does it contain more than one STX? */
	for (; *serialized == STX;)
		serialized++;

	/* count how many times we iterate (package length) */
	int iteration_count = 0;

	/* Write serialized command to pkg->command */
	for (; *serialized != SEP; iteration_count++)
		*_command++ = *serialized++;

	/* Write serialized arguments to pkg->arguments */
	for (; *serialized != SEP; iteration_count++)
		*_arguments++ = *serialized++;

	/* Everything OK */
	return 0;
};

/* Send package (serialized string) over serial */
void send_pkg(int fd, char* pkg) {

	for (; *pkg != '\0'; pkg++)
		serial_send_char(fd, *pkg);
};
