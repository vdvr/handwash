#include <avr/io.h>
#include <avr/interrupt.h>
<<<<<<< HEAD
#include "board.h"
#include "uartNano.h"
#include "buffer.h"
#include "pkg.h"
#include "timer2min.h"
=======
#include "uart.h"
#include "buffer.h"
#include "pkg.h"
#include "msg.h"
#include "peripheral.h"
>>>>>>> 37a9cca1fb1efec95f40e5f90ae3500fb9913219

// ---------------------------------------
// STX, ETX and NULL are defined in pkg.h
// ---------------------------------------

// Global variables ---------------------

// buffer[] char array declared in buffer.h, initialized in buffer.c
// buffer_t int declared in buffer.h, initialized in buffer.c
// buffer_h int declared in buffer.h, initialized in buffer.c
// buffer_used char declared in buffer.h, initialized in buffer.c

// commands[] char array declared in pkg.h, initialized in pkg.c
// arguments[] char array declared in pkg.h, initialized in pkg.c
// new_pkg char declared in pkg.h, initialized in pkg.c
// new_msg char declared in pkg.h, initialized in pkg.c

// Global variables end -----------------


ISR (USART_RX_vect)             // interrupt for uart receive
{
	rpi_avail = 1;
	buffer_write(UDR0);         // write uart data to ringbuffer
    if(UDR0 == ETX)             // listen for ETX --> extra pkg in ringbufffer
    {
        new_pkg ++;
    }
}

ISR(INT0_vect)
{
    //pkg_construct("water","123");
}

// ISR(INT1_vect)
// {
//     pkg_construct("zeep","123");
// }

ISR(TIMER1_COMPA_vect)
{
    toggleSoap();
    stopTimer();
}

int main(void)
{
	sei();
	uartSetup(57600);

	for (;;)
	{
		if (is_faucet_sensor_set())			// checks if object detected at faucet sensor, copy body for external interrupt
		{
			if (!rpi_avail) 
			{
				faucet_on_while_sensor_set();
				continue;
			}

			send_msg(REQUEST_WATER, "");

			if (wait_perm_msg(500))
			{
				faucet_on_while_sensor_set_with_timeout(2000);

				send_msg(WATER_DONE, "");
			}
		}
	}
}
