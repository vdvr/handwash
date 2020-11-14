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