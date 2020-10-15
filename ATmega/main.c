/*
 * les 1 blink.c
 *
 * Created: 19/09/2018 14:32:21
 * Author : r0711421
 */ 

#include <avr/io.h>
#include "board.h"

int main(void)
{
    setup();
    while (1) 
    {
		ledOn(4);
		wait();
		ledOff(4);
		wait();
    }
}

