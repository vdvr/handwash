#include <stdio.h> 
#include <sys/ipc.h> 
#include <sys/msg.h>
#include <stdlib.h>
#include <string.h>

#include "helper.h"
#include "tap.h"

int main(int argc, char *argv[]) {
	if (argc < 3) {
		printf("Usage: %s cmd arguments\n", argv[0]);
		exit(1);
	} else {
		int queue;
		key_t key;
		key = generateKey();
		queue = createQueue(key);
		if (
			(argv[1] == "tap" && argv[2] == "status") ||
			(argv[1] == "t" && argv[2] == "s")
		) {
			getTapState(queue);
		}
	}

	// else {
	// 	key_t key;
	// 	int queue;
	// 	struct msg_buffer out_msg;
	// 	struct msg_buffer in_msg;

	// 	key = generateKey();
	// 	queue = createQueue(key);

	// 	memset(&out_msg.p, 0, sizeof(out_msg.p));
	// 	out_msg.msg_type = 1;
	// 	strcpy(out_msg.p.args, argv[2]);
	// 	out_msg.p.cmd = argv[1][0];
		
	// 	printf("\033[1;35m[TX]\033[0m Sended cmd: %d, and arguments: %s\n\r", 
	// 		out_msg.p.cmd, out_msg.p.args);

	// 	sendMsg(queue, out_msg);

	//==============================================================================
	// 	int result = msgrcv(queue, &in_msg, sizeof(in_msg), 2, 0);

	// 	if(result != -1)
	// 		printf("\033[1;35m[RX]\033[0m Received cmd: %d, and arguments %s\n\r", 
	// 			in_msg.p.cmd, in_msg.p.args);
	// 	return 0;
	//==============================================================================
	// }
};