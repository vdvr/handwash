#include "msg.h"

int rpi_avail;

void send_msg(int cmd, char *args)
{
    char s_cmd[2] = { cmd, '\0' };
    pkg_construct(s_cmd, args);
}

int wait_rec_msg(int cmd, int ms)
{
    int start_time = TCNT1;

    while (1)
    {
        while (!new_msg && (TCNT1 - start_time < ms)); // no check if timer overflow occurs

        if (new_msg) 
        {
            pkg_destruct();
            new_msg = 0;

            switch (commands[0])
            {
                case ACK:
                    return 1;
                case NACK:
                    return 0;
                default:
                    continue;
            }
        }

        rpi_avail = 0;
        return 0;
    }
}