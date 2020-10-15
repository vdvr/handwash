#include "helper.h"
#include "pkg.h"

#include <stdio.h>
#include <pigpio.h>
#include <string.h>
#include <signal.h>

#define BAUDRATE    115200
#define BUFF_SIZE   20

int main() {
	char tx[BUFF_SIZE];
	char rx[BUFF_SIZE];
	char rxptr = 0;

	key_t key = generate_key();
	int queue = create_queue(key);

	int start = 0;
	int count = 0;
	struct Msg rx_msg;
	struct Msg tx_msg;

	int fd = serOpen("/dev/serial0", BAUDRATE, NULL);

	while (1) {
		int result = rcv_msg(queue, &rx_msg, 1);
		if (result != -1) {
			memset(tx, 0, sizeof(tx));
			serialize(rx_msg.pkg, tx);
			send_pkg(fd, tx);
		}
		if (serReadByte(fd) > 0) {
			char c = serReadByte(fd);
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
					int result = deserialize(rx, &tx_msg.pkg);
					if (result != -1) {
						queue = create_queue(key);
						tx_msg.type = 2;
						send_msg(queue, tx_msg);
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
	serClose(fd);
};
