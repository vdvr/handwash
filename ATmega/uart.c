#include <avr/io.h>
#include <avr/interrupt.h>
#include "uart.h"

void uartSetup(long baudrate) {
	DDRD |= (1<<PD1);

	_USART_REGISTER = (int)((F_CPU)/(16*baudrate))-1;

	_USART_UCSRB = (1<<_RXCIE)|(1<<_RXEN)|(1<<_TXEN);
	_USART_UCSRC = (3<<_USART_UCSZ0);
}

void uartPutChar(char data) {
	while ((_USART_UCSRA & (1<<_USART_UDRE))==0);
	_USART_UDR0 = data;
}

void uartPutASCII(unsigned int data) {
	char getal[10];
	int i = 0;

	do {
		getal[i] = data%10;
		data = data / 10;
		i++;
	} while(data != 0);

	while(i > 0) {
		i--;
		uartPutChar(getal[i]+'0');
	}
}
