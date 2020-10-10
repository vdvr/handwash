#include <sys/ipc.h>
#include <sys/msg.h>
#include "msg.h"

enum SUBJ {
	PRESERVED,
	TAP,
	HANDDETECTOR
};
enum HANDDETECTOR {
	HANDDETECTOR_IDLE,
	HANDDETECTOR_DETECTED
};

void pretty_print_msg(struct msg_buffer);

key_t 	generateKey		();
int 	createQueue		(key_t);
void 	destroyQueue	(int);
void 	sendMsg			(int ,struct msg_buffer);
int 	rcvMsg			(int queue, struct msg_buffer *msg, int type);