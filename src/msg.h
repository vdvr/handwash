#ifndef MSG_H_
#define MSG_H_

#include "pkg.h"

#define ACK 0x20
#define NACK 0x21

#define POLL_REQUEST 0x30
#define POLL_REPLY 0x31
#define REQUEST_WATER 0x32
#define REQUEST_SOAP 0x33
#define WATER_DONE 0x34
#define SOAP_DONE 0x35


extern int rpi_avail;

void send_msg(char cmd, char *args);
int wait_rec_msg(int ms, int affermative, int negative);
void reset_msgs_in(void);
    

#endif /* MSG_H_ */