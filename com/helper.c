#include <stdio.h>
#include <sys/ipc.h> 
#include <sys/msg.h>
#include <stdlib.h>

#include "helper.h"
#include "msg.h"
#include "tap.h"

key_t generateKey() {
	return ftok("token", 60);
};

int createQueue(key_t key) {
	return msgget(key, 0666 | IPC_CREAT);
};

void destroyQueue(int queue) {
	msgctl(queue, IPC_RMID, NULL);
};

void sendMsg(int queue, struct msg_buffer msg) {
	msgsnd(queue, &msg, sizeof(msg), 0);
};

int rcvMsg(int queue, struct msg_buffer *msg, int type) {
	return msgrcv(queue, msg, sizeof(struct msg_buffer), type, IPC_NOWAIT);
};

void pretty_print_msg(struct msg_buffer msg) {
	if (msg.p.subj == TAP) {
		printf("TAP ");
		if (msg.p.cmd == TAP_CLOSED)
			printf("CLOSED\n");
		else if (msg.p.cmd == TAP_OPENED)
			printf("OPENED\n");
	} else if(msg.p.subj == HANDDETECTOR) {
		printf("HANDDETECTOR ");
		if (msg.p.cmd == HANDDETECTOR_IDLE)
			printf("IDLE\n");
		else if (msg.p.cmd == HANDDETECTOR_DETECTED)
			printf("DETECTED\n");
	}
	printf("PRESERVED ");
}