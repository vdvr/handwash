#include <avr/io.h>
#include <avr/interrupt.h>
#include "uartNano.h"



void uartSetup(long baudrate)				// works
{
	DDRD |= (1<<PD1);

	UBRR0 = ((F_CPU)/(16*baudrate))-1;		// asynchonous normal speed mode

	UCSR0B = (1<<RXCIE0)|(1<<RXEN0)|(1<<TXEN0);
	UCSR0C = (3<<UCSZ00);
}

void uartPutChar(char data)					// works, sends 1 char at a time
{
    while((UCSR0A & (1<<UDRE0))==0);
	UDR0 = data;
}

void uartPutASCII(int data)					// works
{											// used for debugging and sending values
	char getal[10];
	int i = 0;
	
	do
	{
		getal[i] = data%10;
 		data = data / 10;
		i++;
	}while(data != 0);

	while(i>0)
	{
		i--;
		uartPutChar(getal[i]+'0');
	}
}