#include <avr/io.h>
#include "peripheral.h"


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

void faucet_on_while_sensor_set(void)
{
    int is_on_again = 0;
    faucet_on();

    while (true) 
    {
        is_on_again = 0;
        while (is_faucet_sensor_set());

        int start_time = TCNT1;
        while (TCNT1 - start_time < 2000)  // no check if timer overflow occurs
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

void faucet_on_while_sensor_set_with_timeout(int timeout)
{
    int is_on_again = 0;

    while (true) 
    {
        faucet_on();

        is_on_again = 0;
        while (is_faucet_sensor_set());

        int start_time = TCNT1;
        while (TCNT1 - start_time < 2000)  // no check if timer overflow occurs
        {
            if (is_faucet_sensor_set()) {
                is_on_again = 1;
                break;
            }
        }

        if (is_on_again) continue;
        else faucet_off();

        start_time = TCNT1;
        while (TCNT1 - start_time < timeout)  // no check if timer overflow occurs
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