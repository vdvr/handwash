#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>
#include <sys/poll.h>
#include <unistd.h>
#include <termios.h>
#include <sys/ioctl.h>

#include "helper.h"
#include "pkghandler.h"
#include "serial.h"

#define BUFF_SIZE   100

int main() {
        char tx_buffer[BUFF_SIZE] = {'\0'};
        char rx_buffer[BUFF_SIZE] = {'\0'};

        char* rxpt;
        rxpt = &rx_buffer[0];

        key_t key = generate_key();
        int queue = create_queue(key);

        struct Msg* rx_msg = (struct Msg*) malloc(sizeof(struct Msg));
        struct Msg tx_msg;

        system("sudo stty -F /dev/arduino -hupcl");
        system("chmod a+rw /dev/arduino");
        int fd = serial_open("/dev/arduino");
        tcflush(fd, TCIOFLUSH);

        int busy = 0;
        int num;
        char c;

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
                        c = serial_get_char(fd);
                        if ((c == STX) && !busy) {
                                busy = 1;
                                *rxpt++ = STX; // Read in the whole frame!
                        }
                        while ((c != ETX) && busy) {
                                *rxpt++ = c;
                                c = serial_get_char(fd);
                        }
                        *rxpt++ = ETX;
                        if (c == ETX) {
                                if (deserialize(rx_buffer, &tx_msg.pkg) != -1) {
                                        queue = create_queue(key);
                                        tx_msg.type = 2;
                                        printf("Got message with command: %s and arguments: %s", tx_msg.pkg.command, tx_msg.pkg.arguments);
                                        send_msg(queue, tx_msg);
                                }
                                busy = 0;
                                rxpt = &rx_buffer[0];
                        }
                } else usleep(200);
        }
        close(fd);
};