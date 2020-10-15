#ifndef __PKGSTRUCT__
#define __PKGSTRUCT__

struct Pkg {
	char* command;
	int command_length;
	char* arguments;
	int arguments_length;
};
#endif