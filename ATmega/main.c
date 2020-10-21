#include <avr/io.h>
#include <avr/interrupt.h>
#include "uartNano.h"
#include "buffer.h"
#include "pkg.h"

// ---------------------------------------
// STX, ETX and NULL are defined in pkg.h
// ---------------------------------------

// Global variables ---------------------

// buffer[] char array declared in buffer.h, initialized in buffer.c
// buffer_t int declared in buffer.h, initialized in buffer.c
// buffer_h int declared in buffer.h, initialized in buffer.c
// buffer_used char declared in buffer.h, initialized in buffer.c

// commands[] char array declared in pkg.h, initialized in pkg.c
// arguments[] char array declared in pkg.h, initialized in pkg.c
// new_pkg char declared in pkg.h, initialized in pkg.c
// new_msg char declared in pkg.h, initialized in pkg.c

// Global variables end -----------------


ISR (USART_RX_vect)             // interrupt for uart receive
{
	buffer_write(UDR0);         // write uart data to ringbuffer
    if(UDR0 == ETX)             // listen for ETX --> extra pkg in ringbufffer
    {
        new_pkg ++;
    }
}

int main(void)
{
    uartSetup(57600);

    for (;;)
    {
        sei();
        if(new_pkg) 
        {
            pkg_destruct();
        }
        if(new_msg)
        {   
            // code here for interpreting the new msg
            new_msg = 0;


            pkg_construct("123","123");
        }
    }
    
}