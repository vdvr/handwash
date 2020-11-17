#include <avr/io.h>
#include <avr/interrupt.h>

#include "buffer.h"
#include "pkg.h"
#include "timer2min.h"
#include "msg.h"
#include "peripheral.h"
#include "uart.h"
#include "debug.h"

#define RPI_TIMEOUT_MS 5000			// time to wait for RPI response, high to test
#define POLL_TIMEOUT_S 10			// time after last action to send POLL request, low to test

// ---------------------------------------
// STX, ETX and SEP are defined in pkg.h
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

// seconds_now declared in timer2min.h, initialized in timer2min.c
//unsigned int seconds_now;

// Global variables end -----------------


ISR (USART_RX_vect)             // interrupt for uart receive
{
	char c = _USART_UDR0;

	buffer_write(c);         // write uart data to ringbuffer
	if(c == ETX)             // listen for ETX --> extra pkg in ringbufffer
	{
		new_pkg ++;
	}
}

ISR(TIMER1_COMPA_vect)
{
    seconds_now++;
	poll_sec++;
}

int main(void)
{
	sei();

	//debug_port_setup();

	peripheral_setup();
	uartSetup(9600);
	timerSetup();
	startTimer();
	rpi_avail = 1;

	for (volatile long j = 0; j < 1000000; j++);		// make custom delay function based on timer?31
	//debug_sendString("init");

	for (;;)
	{

		//if(debug_port_read(0)) pkg_construct("water","");


		if (is_faucet_sensor_set())			// checks if object detected at faucet sensor, copy body for external interrupt
		{
			//debug_sendString("faucet detected");
			if (!rpi_avail)
			{
				//debug_sendString("rpi not avail");
				faucet_on_while_sensor_set();
				resetPollTimer();
				continue;
			}

			else
			{
				//debug_sendString("rpi avail");
				resetTimer();					// only reset if rpi available
				reset_msgs_in();
				send_msg(REQUEST_WATER, "");
				
				int result = wait_rec_msg(RPI_TIMEOUT_MS, ACK, NACK);
				if (result == 1)
				{
					//debug_sendString("ack rec");
					faucet_on_while_sensor_set_with_timeout(2000);

					send_msg(WATER_DONE, "");
				} 
				else if (result == -1) 
				{
					for (volatile long j = 0; j < 500000; j++);		// delay om niet constant naar water te vragen indien geen toestemming
				}
			}
		}

		

		else if (is_soap_sensor_set())
		{
			//debug_sendString("soap detected");
			if (!rpi_avail)
			{
				//debug_sendString("rpi not avail");
				soap_on_while_sensor_set();
				resetPollTimer();
				continue;
			}

			else
			{
				//debug_sendString("rpi avail");
				resetTimer();					// only reset if rpi available
				reset_msgs_in();
				send_msg(REQUEST_SOAP, "");
				
				int result = wait_rec_msg(RPI_TIMEOUT_MS, ACK, NACK);
				if (result == 1)
				{
					//debug_sendString("ack rec");
					soap_on_while_sensor_set();

					send_msg(SOAP_DONE, "");
				} 
				else if (result == -1) 
				{
					for (volatile long j = 0; j < 500000; j++);		// delay om niet constant naar zeep te vragen indien geen toestemming
				}
			}
		}

		else if ((!rpi_avail) && (poll_sec >= POLL_TIMEOUT_S))
		{
			resetTimer();                       // wait_rec_msg gebruikt timestamps
			reset_msgs_in();
			send_msg(POLL_REQUEST,"");
			rpi_avail = wait_rec_msg(RPI_TIMEOUT_MS, POLL_REPLY, NACK); //
			resetPollTimer();                       // voor volgende poll, voor als de poll faalde
			// if (rpi_avail) debug_sendString("rpi avail");
			// else debug_sendString("rpi not avail");
		}
	}
}