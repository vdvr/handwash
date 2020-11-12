#include <avr/io.h>
#include "timer2min.h"

unsigned int seconds_now = 0;

void timerSetup(void)
{
    TCCR1A = 0;
    OCR1A = TIMER_OF_1HZ;                      // compare value for 1Hz
    TIMSK1 |= (1<<OCIE1A);                // compare match interrupt
    TCCR1B |= (1<<WGM12);
    //TCCR1B |= (1<<CS12);              // by connecting prescaler timer starts to count
}

void stopTimer(void)                    // worden niet gebruikt
{
    TCCR1B &= ~(1<<CS12);
}

void startTimer(void)                   // word enkel na setup gebruikt
{
    TCCR1B |= (1<<CS12);
}

void resetTimer(void)                   // worden niet gebruikt
{
    seconds_now = 0;
    TCNT1 = 0;
}

struct timestamp getTime(void)
{
    return (struct timestamp) {
        .seconds = TCNT1,
        .extra = seconds_now
    };
}

int checkTimeElapsed(struct timestamp time, unsigned int seconds, unsigned int extra) 
{
    unsigned int total_extra;
    unsigned int extra_now = TCNT1; // store in case overflows between 2 if statements
    unsigned int total_seconds = time.seconds + seconds;

    if (total_seconds > seconds_now) 
    {
        return 1;
    }

    total_extra = time.extra + extra; // calculate only if needed
    if ((total_seconds == seconds_now) || (total_extra >= extra_now))
    {
        return 1;
    }

    return 0;
}