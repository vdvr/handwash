#include <avr/io.h>
#include <avr/interrupt.h>
#include "uartNano.h"
#include "buffer.h"

#define STX 'a'
#define ETX 'b'
#define NULL 32

char commands[20];
char arguments[20];

char new_pkg = 0;
char new_msg = 0;

char length = 0;

char pkg[40];

ISR (USART_RX_vect)
{
	buffer_write(UDR0);
    if(UDR0 == ETX) 
    {
        new_pkg ++;
    }
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
                //uartPutChar(command);             // for debugging
                if(command==NULL) break;
            }
        }
    for (int i = 0; i < 20; i++)
        {
            char argument = buffer_read();
            arguments[i] = argument;
            if((argument==ETX) | (argument == 0)) break;
        }
    new_pkg --;
    new_msg = 1;
}

int main(void)
{
    uartSetup(57600);

    for (;;)
    {
        sei();
        if(new_pkg) pkg_read();
        if(new_msg)
        {   
            // uartPutChar('x');
            // uartPutASCII(length);
            // for(int i = 0; i<64; i++)
            // {
            //     uartPutChar(buffer[i]);
            // }
             uartPutChar(commands[0]);          // doet geen print commands
             uartPutChar(commands[1]);
             uartPutChar(commands[2]);
            new_msg = 0;
        }
    }
    
}