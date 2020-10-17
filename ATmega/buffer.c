#include <avr/io.h>
#include "uartNano.h"

#include "buffer.h"

char buffer[BUFFER_SIZE];
int buffer_t = 0;              // buffer tail index
int buffer_h = 0;              // buffer head index
char buffer_used = 0;       // to keep track of filled space

void buffer_write(char data)         // fill buffer with uart data, function in ISR
{
    if(buffer_used < BUFFER_SIZE)       // buffer not full
    {
        buffer[buffer_h] = data;            // write to ringbuf on head-index
        buffer_h++;                         // increment head index
        buffer_h &= (BUFFER_SIZE);      // ringbuf wraparound
        buffer_used++;                      // increment bufferspace used
    }
}

char buffer_read()
{
    if((buffer_h == buffer_t) && (buffer_used <= 0)) return 0;        // buffer empty

    char data = buffer[buffer_t];       // read buffer at tail
    buffer_t++;                         // move tail
    buffer_t &= BUFFER_SIZE;            // tail wraparound
    buffer_used--;                      // decrement bufferused
    return data;           // succesfully read buffer
}