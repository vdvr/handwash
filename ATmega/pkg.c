#include <avr/io.h>
#include "uart.h"       // included for debugging
#include "buffer.h"
#include "pkg.h"

char commands[20];          // commands out of destructed pkg
char arguments[20];         // arguments out of destructed pkg

char new_pkg = 0;           // amount of packages in ring buffer according to STX in ISR()
char new_msg = 0;           // message is read, can find data in commands[] and arguments[]

void pkg_destruct()
{
    while(buffer_used > 0 && buffer_read() != STX);     // zoek achter package in buffer
    for (int i = 0; i < 20; i++)
        {
            if(buffer_used>0)           // buffer not empty
            {
                char command = buffer_read();
                commands[i] = command;
                //uartPutChar(command);             // for debugging
                if(command==NULL) break;        // null is the seperator
            }
        }
    //uartPutChar('x');
    for (int i = 0; i < 20; i++)
        {
            if(buffer_used>0)       // buffer not empty
            {
                char argument = buffer_read();
                arguments[i] = argument;
                //uartPutChar(argument);             // for debugging
                if((argument==ETX) | (argument == 0)) break;    // ETX is the end of pkg, 0 means empty buffer space (error)
            }
        }
    new_pkg --;
    new_msg = 1;
}

void pkg_construct(char* cmd, char* arg)        // works, attention to constructors for actual messages (now for serialtools testing)
{
    uartPutChar(STX);
    for(int i = 0; i<20; i++)
    {
        if(*cmd == 0)break;
        uartPutChar(*cmd);
        cmd++;
    }
    uartPutChar(NULL);
    for(int i = 0; i<20; i++)
    {
        if(*arg == 0)break;
        uartPutChar(*arg);
        arg++;
    }
    uartPutChar(ETX);
}
