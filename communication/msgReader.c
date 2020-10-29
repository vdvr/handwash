#include <stdio.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <string.h>
#include "helper.h"

int main() {
	key_t key;
	int msgid;

	struct Msg msg;
	key = generate_key();
	msgid = create_queue(key);
	memset(&msg, 0, sizeof(msg));

	int result = msgrcv(msgid, &msg, sizeof(msg), 2, IPC_NOWAIT);

	if (result != -1) {
		// Print
	}
	destroy_queue(msgid);

	return 0;
};