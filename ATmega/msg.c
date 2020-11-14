#include "msg.h"
#include "timer2min.h"
#include "buffer.h"

int rpi_avail;


void send_msg(char cmd, char *args)
{
    char s_cmd[2] = { cmd, '\0' };
    pkg_construct(s_cmd, args);
}


int wait_rec_msg(int ms, int affermative, int negative)
{
    unsigned long secs, extra;
    struct timestamp time = getTime();

    while (1)
    {
        secs = ms / 1000;
        extra = (ms % 1000) * TIMER_OF_1HZ / 1000;
        while ((new_pkg == 0) && !checkTimeElapsed(time, secs, extra));


        if (new_pkg > 0) 
        {
            pkg_destruct();
            new_msg = 0;

            if (commands[0] == affermative) 
            {
                return 1;
            }
            else if (commands[0] == negative)
            {
                return -1;
            }
            else 
            {
                continue;           // ignore irrelevant commands
            }
        }

        rpi_avail = 0;
        return 0;
    }
}


void reset_msgs_in(void) 
{
    new_pkg = 0;
    buffer_t = 0;
    buffer_h = 0;
    buffer_used = 0; 
}