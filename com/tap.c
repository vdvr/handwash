#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "helper.h"
#include "tap.h"

void getTapState(int queue) {
	struct msg_buffer pkg;
	memset(&pkg.p, 0, sizeof(pkg.p));

	pkg.p.subj = TAP;
	pkg.p.cmd = TAP_STATE;

	sendMsg(queue, pkg);
};