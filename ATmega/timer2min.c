#include <avr/io.h>
#include "timer2min.h"

unsigned int seconds_now = 0;
unsigned int poll_sec;

void timerSetup(void)
{
    TCCR1A = 0;
    OCR1A = TIMER_OF_1HZ;                      // compare value for 1Hz
    TIMSK1 |= (1<<OCIE1A);                // compare match interrupt
    TCCR1B |= (1<<WGM12);
}

void stopTimer(void)                    // worden niet gebruikt
{
    TCCR1B &= ~(5<<CS10);
}

void startTimer(void)                   // word enkel na setup gebruikt
{
    TCCR1B |= (5<<CS10);                // by connecting prescaler timer starts to count
}

void resetTimer(void)
{
    disableTimerIR();
    seconds_now = 0;
    TCNT1 = 0;
    enableTimerIR();
}

void resetPollTimer(void)
{
    disableTimerIR();
    poll_sec = 0;
    enableTimerIR();
}

void enableTimerIR(void)
{
    TIMSK1 |= (1<<OCIE1A);
}

void disableTimerIR(void)
{
    TIMSK1 &= ~(1<<OCIE1A);
}

struct timestamp getTime(void)
{
    disableTimerIR();
    struct timestamp time_now = {
        .seconds = seconds_now,
        .extra = TCNT1,
    };
    enableTimerIR();

    return time_now;
}

int checkTimeElapsed(struct timestamp time_past, unsigned int seconds, unsigned int extra) 
{
    unsigned int total_extra, total_seconds;
    struct timestamp time_now = getTime();
    
    total_extra = time_past.extra + extra;
    total_seconds = time_past.seconds + seconds + (total_extra / TIMER_OF_1HZ);
    total_extra %= TIMER_OF_1HZ;

    if (total_seconds < time_now.seconds) 
    {
        return 1;
    }

    if ((total_seconds == time_now.seconds) && (total_extra <= time_now.extra))
    {
        return 1;
    }

    return 0;
}