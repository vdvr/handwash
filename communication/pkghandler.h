#include "pkg.h"

#define STX 2
#define ETX 3

void 	serialize	(struct Pkg* pkg  , char* serialized);
int 	deserialize	(char* serialized, struct Pkg* pkg);
void 	send_pkg 	(int 	i     	 , char* serialized);
