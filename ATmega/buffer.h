#ifndef BUFFER_H_
#define BUFFER_H_

#include <avr/io.h>
#include "uartNano.h"

#define BUFFER_SIZE 64          // ringbuffer size must be power of 2 for easy wraparound

extern char buffer[BUFFER_SIZE];
extern int buffer_t;              // buffer tail index
extern int buffer_h;              // buffer head index
extern char buffer_used;       // to keep track of filled space

void buffer_write(char);        // writes uart data to ringbuffer

char buffer_read(void);         // reads ringbuffer

#endif /* BUFFER_H_ */