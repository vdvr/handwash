#include "helper.h"
#include "pkg.h"

#include <stdio.h>
#include <wiringSerial.h>
#include <string.h>
#include <signal.h>

#define BAUDRATE    9600
#define BUFF_SIZE   20

int main() {
	char tx[BUFF_SIZE];
	char rx[BUFF_SIZE];
	char rxptr = 0;

	key_t key = generateKey();
	int queue = createQueue(key);

	int start = 0;
	int count = 0;
	struct msg_buffer rx_msg;
	struct msg_buffer tx_msg;

	int fd = serialOpen("/dev/serial0", BAUDRATE);
	serialFlush(fd);

	while (1) {
		int result = rcvMsg(queue, &rx_msg, 1);
		if (result != -1) {
			memset(tx, 0, sizeof(tx));
			construct(rx_msg.p, tx);
			send_pkg(fd, tx);
		}
		if (serialDataAvail(fd) > 0) {
			char c = serialGetchar(fd);
			if ((c==2) && (start ==0)) {
				memset (rx, 0, sizeof(rx));
				start=1;
				rxptr=0;
			}
			rx[rxptr++] = c;
			if (rxptr == 2)
				count = (int) c;
			if (rxptr == count+3) {
				if (c == 3) {
					rx[rxptr++] = c;
					int result = destruct(rx, &tx_msg.p);
					if (result != -1) {
						queue = createQueue(key);
						tx_msg.msg_type = 2;
						sendMsg(queue, tx_msg);
					}
					start = count = 0;
				}
				else {
					printf("\n\r\033[1;31m[ERROR]\033[0m Package Corrupt\n\r");
					start = count = rxptr = 0;
				}
			}
		}
	}
};
