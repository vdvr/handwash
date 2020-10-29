#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <wiringSerial.h>
#include <signal.h>
#include <sys/poll.h>
#include <unistd.h>
#include "helper.h"
#include "pkghandler.h"

#define BAUDRATE    115200
#define BUFF_SIZE   100

int main() {
        char tx_buffer[BUFF_SIZE];
        char rx_buffer[BUFF_SIZE];

        char* rxpt;
        rxpt = &rx_buffer[0];

        key_t key = generate_key();
        int queue = create_queue(key);

        struct Msg* rx_msg = (struct Msg*) malloc(sizeof(struct Msg));
        struct Msg tx_msg;
        system("sudo stty -F /dev/arduino -hupcl");

        int fd = serialOpen("/dev/arduino", BAUDRATE);
        system("chmod a+rw /dev/ttyACM0");

        serialFlush(fd);

        int busy = 0;
        char c;

        while (1) {
                int result = rcv_msg(queue, rx_msg, 1);
                if (result != -1) {
                        memset(tx_buffer, 0, sizeof(tx_buffer));
                        serialize(&rx_msg->pkg, &tx_buffer[0]);
                        send_pkg(fd, tx_buffer);
                }
                if (serialDataAvail(fd) > 0) {
                        c = serialGetchar(fd);
                        if ((c == STX) && !busy) {
                                printf("Receiving PKG\n");
                                busy = 1;
                                *rxpt++ = STX; // Read in the whole frame!
                        }
                        while ((c = serialGetchar(fd) != ETX) && busy) {
                                *rxpt++ = c;
                        }
                        if (c == ETX) {
                                if (deserialize(rx_buffer, &tx_msg.pkg) != -1) {
                                        queue = create_queue(key);
                                        tx_msg.type = 2;
                                        send_msg(queue, tx_msg);
                                } else {
                                        printf("\n\r\033[1;31m[ERROR]\033[0m Package Corrupt\n\r");
                                }
                                busy = 0;
                                rxpt = &rx_buffer[0];
                        }
                }
                else usleep(200);
        }
        serialClose(fd);
};
