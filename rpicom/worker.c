#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>
#include <sys/poll.h>
#include <unistd.h>
#include <termios.h>
#include <sys/ioctl.h>
#include <zmq.h>

#include "helper.h"
#include "pkghandler.h"
#include "serial.h"

#define BUFF_SIZE   100
#define PYTHON_QUEUE_KEY 12345

int read_until_start(int fd);
int read_pkg(int fd, char* buff);
int check_pkg(char* rxpt);

int main() {

	/* Create tx and rx buffer, fill them with zero's */
        char tx_buffer[BUFF_SIZE] = {'\0'};
        char rx_buffer[BUFF_SIZE] = {'\0'};

	/* Make pointer rxpt to iterate over rx_buffer */
        char* rxpt;
        rxpt = &rx_buffer[0];

	/* Create a new POSIX message queue */
        int queue = create_queue();

	/* Create msg structs for IPC messaging */
        struct Msg* rx_msg = (struct Msg*) malloc(sizeof(struct Msg)); 
	struct Msg tx_msg;

	/* Setup the arduino - Needs su! */
        system("sudo stty -F /dev/arduino -hupcl");
        system("chmod a+rw /dev/arduino");

	/* Get arduino file descriptor */
        int fd = serial_open("/dev/arduino");

	/* Flush the data already in buffer */
        tcflush(fd, TCIOFLUSH);

        int busy = 0;
        int num;
        char c;

	/* Python end POSIX message queue */
	int pyid = msgget( (key_t)PYTHON_QUEUE_KEY, IPC_CREAT | 0666);

        while (1) {
                int result = rcv_msg(queue, rx_msg, 1);
                if (result != -1) {
                        memset(tx_buffer, 0, sizeof(tx_buffer));
                        serialize(&rx_msg->pkg, &tx_buffer[0]);
                        send_pkg(fd, tx_buffer);
                }
                if (ioctl (fd, FIONREAD, &num) == -1)
                        break;
                if (num > 0) {

			/* Wait until start */
			read_until_start(fd);
			
			/* We are pass the STX */
			*rxpt++ = STX;
			
			/* Read all the data into rx_buffer */
			read_pkg(fd, rxpt);

			/* Send the tx_msg message to the python queue */
			tx_msg.type = 2;
			if (deserialize(rx_buffer, &tx_msg.pkg) != -1)
				msgsnd( pyid, &tx_msg, sizeof(struct Pkg), tx_msg.type);
			rxpt = &rx_buffer[0];
                } 
		else 
			usleep(50);
        }
        close(fd);
};

int read_until_start(int fd) {

	char c = 0;
	if (c != STX)
		c = serial_get_char(fd);
	return 0;
}

int read_pkg(int fd, char* buff) {

	char c = 0;
	for (; c != ETX; c = serial_get_char(fd))
		*buff++ = c;

	/* c needs to be ETX */
	*buff++ = ETX;

	/* We are done */
	return 0;
}

// int check_pkg(char* buff) {
// 
// 	/* Package needs to end with ETX */
// 	if (*buff-- != ETX)
// 		return 1;
// 	
// 	/* Arguments may not exceed bounds
// 	 * And also this checks if there is a \r separator */
// 	int count = 0;
// 	for (; *buff-- != '\r'; count++)
// 		if (count > BUFF_SIZE) return 1;
// 
// 	/* Command may not exceed bounds and package needs to end with ETX */
// 	count = 0;
// 	for (; *buff-- != STX; count++)
// 		if (count > BUFF_SIZE) return 1;
// 
// 	return 0;
// }

