#include <avr/io.h>
#include "peripheral.h"
#include "timer2min.h"


void peripheral_setup(void)
{
    F_DDR |= (1 << F_PIN);
    S_DDR |= (1 << S_PIN);
    F_S_DDR |= (1 << F_S_PIN);
    S_S_DDR |= (1 << S_S_PIN);
}

int is_faucet_sensor_set(void) 
{
    return F_S_DDR && (1 << F_S_PIN);
}

void faucet_on(void) 
{
    F_PORT |= (1 << F_PIN);
}

void faucet_off(void)
{
    F_PORT &= ~(1 << F_PIN);
}

// sets faucet on, stays on aslong as faucet_sensor detects
// and until sensor doesnt detect for 2 seconds, then faucet off and exiting
void faucet_on_while_sensor_set(void)
{
    int is_on_again = 0;
    struct timestamp start_time;

    faucet_on();

    while (true) 
    {
        is_on_again = 0;
        while (is_faucet_sensor_set());

        start_time = getTime();
        while (!checkTimeElapsed(start_time, 2, 0))
        {
            if (is_faucet_sensor_set()) {
                is_on_again = 1;
                break;
            }
        }

        if (is_on_again) continue;

        faucet_off();
        return;   
    }
}

// sets faucet on, stays on aslong as faucet_sensor detects
// and until sensor doesnt detect for 2 seconds, then faucet off
// finally timeout will decide how long sensor has time to detect again and repeat cycle
// if no detection in timout span, function exited
void faucet_on_while_sensor_set_with_timeout(int timeout)
{
    struct timestamp start_time;
    unsigned int timeout_s = timeout / 1000;
    unsigned int timout_e = (timeout % 1000) * TIMER_OF_1HZ / 1000; // convert ms to extra
    int is_on_again = 0;

    while (true) 
    {
        faucet_on();

        is_on_again = 0;
        while (is_faucet_sensor_set());

        // keep faucet until nothing detected for 2 seconds
        start_time = getTime();
        while (!checkTimeElapsed(start_time, 2, 0))
        {
            if (is_faucet_sensor_set()) {
                is_on_again = 1;
                break;
            }
        }

        if (is_on_again) continue;
        else faucet_off();

        start_time = getTime();
        while (!checkTimeElapsed(start_time, timeout_s, timout_e))
        {
            if (is_faucet_sensor_set()) {
                is_on_again = 1;
                break;
            }
        }

        if (is_on_again) continue;
        else return;
    }
}