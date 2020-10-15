#include "pkg.h"

void 	serialize	(struct Pkg	pkg  , char* serialized);
int 	deserialize	(char* serialized, struct Pkg* pkg);
void 	send_pkg 	(int 	i     	 , char* serialized);
