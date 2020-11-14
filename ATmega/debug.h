#ifndef DEBUG_H_
#define DEBUG_H_

void debug_sendString(char* txt);

void debug_port_setup (void);

char debug_port_read (char pin);

#endif /* DEBUG_H_ */