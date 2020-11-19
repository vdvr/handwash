#include "pkg.h"

#define STX '\x02'
#define ETX '\x03'
#define SEP '\r'

void 	serialize	(struct Pkg* pkg, char* serialized);
int 	deserialize	(char* serialized, struct Pkg* pkg);
void 	send_pkg 	(int fd, char* serialized);
