#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdarg.h>
#include <string.h>
#include <termios.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <sys/types.h>
#include <sys/stat.h>

#include "serial.h"

#ifndef DEBUG
#define DEBUG 0
#endif

/* TODO documentate */

int serial_open(const char *device) {
        struct termios options;
        speed_t myBaud = B9600;
        int     status, fd;

        if ((fd = open (device, O_RDWR | O_NOCTTY | O_NDELAY | O_NONBLOCK)) == -1)
                return -1;

        fcntl (fd, F_SETFL, O_RDWR);
        tcgetattr (fd, &options);

        cfmakeraw   (&options);
        cfsetispeed (&options, myBaud);
        cfsetospeed (&options, myBaud);

        options.c_cflag |= (CLOCAL | CREAD);
        options.c_cflag &= ~PARENB;
        options.c_cflag &= ~CSTOPB;
        options.c_cflag &= ~CSIZE;
        options.c_cflag |= CS8;
        options.c_lflag &= ~(ICANON | ECHO | ECHOE | ISIG);
        options.c_oflag &= ~OPOST;

        options.c_cc [VMIN]  =   0;
        options.c_cc [VTIME] = 100;	// Ten seconds (100 deciseconds)

        tcsetattr (fd, TCSANOW, &options) ;

        ioctl (fd, TIOCMGET, &status);

        status |= TIOCM_DTR ;
        status |= TIOCM_RTS ;

        ioctl (fd, TIOCMSET, &status);

        usleep(10000);	// 10ms

        return fd;
}

int serial_get_char(const int fd) {
        unsigned int x ;

        if (read (fd, &x, 1) != 1)
                return -1;
	
	/* print message if wanted */
	if (DEBUG)
		fprintf(stderr, "[DBG: SERIAL] %c\n", ((int)x & 0xFF));

        return ((int)x) & 0xFF;
}

void serial_send_char(const int fd, const unsigned char c) {
        write (fd, &c, 1) ;
}
