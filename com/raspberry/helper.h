#include <sys/ipc.h>
#include <sys/msg.h>
#include "msg.h"

void pretty_print_msg(struct Msg);

key_t 	generate_key	();
int 	create_queue	(key_t);
void 	destroy_queue	(int);
void 	send_msg		(int ,struct Msg);
int 	rcv_msg			(int queue, struct Msg *msg, int type);
void 	pp 				(struct Msg* msg);