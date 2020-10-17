#include <avr/io.h>
#include <avr/interrupt.h>
#include "uartNano.h"
#include "buffer.h"

#define STX 2
#define ETX 3

char commands[20];
char arguments[20];

char cmd_start = 0;

char pkg[40];

ISR (USART_RX_vect)
{
	buffer_write(UDR0);
}

void pkg_read()
{
    while(buffer_used > 0 && buffer_read() != STX);     // zoek achter package in buffer
    for (int i = 0; i < 20; i++)
        {
            if(buffer_used>0)
            {
                char command = buffer_read();
                commands[i] = command;
                if(command==0) break;
            }
        }
    for (int i = 0; i < 20; i++)
        {
            char argument = buffer_read();
            arguments[i] = argument;
            if((argument==ETX) | (argument == 0)) break;
        }

}

int main(void)
{
    uartSetup(57600);

    for (;;)
    {
        sei();

    }
    
}