#ifndef __MSG__
#define __MSG__

#include "pkgstruct.h"
struct msg_buffer { 
	long msg_type; 
	struct package p; 
}; 
#endif