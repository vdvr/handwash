#include <avr/io.h>
#include "peripheral.h"
#include "timer2min.h"


void peripheral_setup(void)
{
    F_DDR |= (1 << F_PIN);              // output
    S_DDR |= (1 << S_PIN);              // output

    F_S_DDR &= ~(1 << F_S_PIN);         // input
    S_S_DDR &= ~(1 << S_S_PIN);         // input
    F_S_PORT |= (1 << F_S_PIN);         // pullup
    S_S_PORT |= (1 << S_S_PIN);         // pullup
}

int is_faucet_sensor_set(void) 
{
    return ((F_S_PORT_PIN & (1 << F_S_PIN)) == 0);      // was eerst !=0 dan is het voor hoog actief
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
    unsigned int timeout_e = (timeout % 1000) * TIMER_OF_1HZ / 1000; // convert ms to extra
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
        while (!checkTimeElapsed(start_time, timeout_s, timeout_e))
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

//-------------- SOAP -------------

int is_soap_sensor_set(void) 
{
    return ((S_S_PORT_PIN & (1 << S_S_PIN)) == 0);      // was eerst !=0 dan is het voor hoog actief
}

void soap_on(void) 
{
    S_PORT |= (1 << S_PIN);
}

void soap_off(void)
{
    S_PORT &= ~(1 << S_PIN);
}

void soap_on_while_sensor_set(void)
{
    struct timestamp start_time;

    // start_time = getTime();                     // voorstel: voor kijken of de sensor geset is, voorkomen zeep naast hand.
    // while(true)
    // {
    //     if(checkTimeElapsed(start_time,5,0)) return;
    //     if(is_soap_sensor_set()) break;
    // }

    start_time = getTime();
    soap_on();
    while(!checkTimeElapsed(start_time, 2, 0));
    soap_off();

    start_time = getTime();
    while(true)                                 // wachten to zeep sensor niet meer geset is want anders gaan ze meer zeep krijgen als rpi_not avail
    {
        if(!is_soap_sensor_set()) break;        // wachten in de stap is niet erg voor rpi, soap done word pas hierna gestuurd
    }

    // voorstel: hier send msg
}