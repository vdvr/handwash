#include <stdio.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <stdlib.h>
#include <string.h>

#include "helper.h"

void get_tap_state(struct Pkg* pkg);

int main(int argc, char *argv[]) {
	if (argc < 3) {
		printf("Usage: %s cmd arguments\n", argv[0]);
		exit(1);
	} else {
		int queue;
		queue = create_queue();

		struct Msg* msg_to_send = (struct Msg*) malloc(sizeof(struct Msg));
		msg_to_send->type = 1;
		strncpy(msg_to_send->pkg.command, "ABC\0", 4);
		strncpy(msg_to_send->pkg.arguments, "D1F\0", 4);

		send_msg(queue, *msg_to_send);
	}
	return 0;
};
