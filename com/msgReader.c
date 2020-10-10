#include <stdio.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <string.h>
#include "helper.h"

int main() {
	key_t key;
	int msgid;

	struct msg_buffer msg;
	key = generateKey();
	msgid = createQueue(key);
	memset(&msg, 0, sizeof(msg));

	int result = msgrcv(msgid, &msg, sizeof(msg), 2, IPC_NOWAIT);

	if (result != -1) {
		printf("Received: ");
		pretty_print_msg(msg);
	}
	destroyQueue(msgid);

	return 0;
};