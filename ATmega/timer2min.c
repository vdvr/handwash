#include <avr/io.h>
#include "timer2min.h"

char seconds = 0;

void secTimerSetup(void)
{
    TCCR1A = 0;
    OCR1A = 31249;                      // compare value for 1Hz
    TIMSK1 |= (1<<OCIE1A);                // compare match interrupt
    //TCCR1B |= (1<<CS12);              // by connecting prescaler timer starts to count
}

void stopTimer(void)
{
    TCCR1B &= ~(1<<CS12);
}

void startTimer(void)
{
    TCCR1B |= (1<<CS12);
}

void resetTimer(void)
{
    TCNT1 = 0;
}