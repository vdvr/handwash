#include <avr/io.h>
#include "uart.h"

void debug_sendString(char* txt)
{
    while(*text1 != 0)
	{
		uartPutChar(*txt);
	}
}