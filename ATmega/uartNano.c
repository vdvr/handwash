#include <avr/io.h>
#include <avr/interrupt.h>
#include "uartNano.h"

void uartSetup(long baudrate)
{
	DDRD |= (1<<PD1);

	UBRR0 = ((F_CPU)/(16*baudrate))-1;		// asynchonous normal speed mode

	UCSR0B = (1<<RXCIE0)|(1<<RXEN0)|(1<<TXEN0);
	UCSR0C = (3<<UCSZ00);
}

void uartPutChar(char data)
{
    while((UCSR0A & (1<<UDRE0))==0);
	UDR0 = data;
}

