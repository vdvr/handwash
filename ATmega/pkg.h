#ifndef PKG_H_
#define PKG_H_

#include <avr/io.h>

#define STX 'a'         // should be 2, temp char a for testing with serialtools
#define ETX 'b'         // should be 3, temp char b for testing with serialtools
#define NULL '0'        // schould be 0, temp char 0 for testing with serialtools

extern char commands[20];       // declaration of arrays, initialized in pkg.c
extern char arguments[20];

extern char new_pkg;        // declaration of var, initialized in pkg.c
extern char new_msg;

void pkg_destruct(void);

void pkg_construct(void);

#endif /* PKG_H_ */