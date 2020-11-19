#include <avr/io.h>
#include "uart.h"

void debug_sendString(char* txt)
{
    while(*txt != 0)
	{
		uartPutChar(*txt++);
	}
	uartPutChar('\3');
}

void debug_port_setup (void)
{
	DDRB = 0;	// allemaal ingangen
	PORTB |= 0b00001111; // PB0 -> PB3 hebben pullups
}

char debug_port_read (char pin)
{
	return ((PINB & (1 << pin)) != 0);
}