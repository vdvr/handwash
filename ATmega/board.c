#include <avr/io.h>
#include <avr/interrupt.h>
#include "board.h"

/*
        file for prototype board
        pins used are:
            - PD0 --> RX
            - PD1 --> TX
            - PD2 --> BUTTON, INTO (hardware interupt)
            - PD3 --> BUTTON, INT1 (hardware interupt)
            - PD5 --> LED, OC0B
            - PD7 --> LED
*/

void boardSetup(void)
{
    DDRD |= (1<<PD1)|(1<<PD5)|(1<<PD7);         // 1 is output
    PORTD |= (1<<PD2)|(1<<PD3);             // pullups on inputs

    EIMSK |= (1<<INT0)|(1<<INT1);
    EICRA = (2<<ISC00)|(2<<ISC10);          // enable external int0 en int1, both as falling edge (because of pullups)
}

void toggleSoap(void)
{
    PORTD ^= (1<<PD5);
}

void toggleWater(void)
{
    PORTD ^= (1<<PD7);
}