#include <stdio.h>
#include <sys/ipc.h> 
#include <sys/msg.h>
#include <stdlib.h>

#include "helper.h"
#include "msg.h"

int create_queue() {
	return msgget(778899, 0666 | IPC_CREAT);
};

void destroy_queue(int queue) {
	msgctl(queue, IPC_RMID, NULL);
};

void send_msg(int queue, struct Msg msg) {
	msgsnd(queue, &msg, sizeof(msg), 0);
};

int rcv_msg(int queue, struct Msg *msg, int type) {
	return msgrcv(queue, msg, sizeof(struct Msg), type, IPC_NOWAIT);
};
