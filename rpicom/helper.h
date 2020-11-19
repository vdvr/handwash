#include <sys/ipc.h>
#include <sys/msg.h>
#include "msg.h"

#define QUEUE_KEY 778899

int 	create_queue	();
void 	destroy_queue	(int);
void 	send_msg	(int ,struct Msg);
int 	rcv_msg		(int queue, struct Msg *msg, int type);
void 	pp 		(struct Msg* msg);
