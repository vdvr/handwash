#include "pkgstruct.h"

int 	calc_crc	(int subj 				, int cmd);
void 	construct	(struct package 		, char*);
int 	destruct 	(char* pakket			, struct package *command);
void 	send_pkg 	(int 					, char*);