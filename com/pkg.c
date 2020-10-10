#include <wiringSerial.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include "pkg.h"

#define STX 2
#define ETX 3

int calc_crc(int i, int j) {
	return STX+ETX+i+j;
};

void construct(struct package p, char* pkg) {
	char subj[2];
	char cmd[2];
	snprintf(subj, 2, "%d", p.subj);
	snprintf(cmd, 2, "%d", p.cmd);

	*pkg++ = STX;
	*pkg++ = subj;
	*pkg++ = cmd;
	*pkg++ = calc_crc(p.subj, p.cmd);
	*pkg++ = ETX;
	*pkg++ = 0;
};

int destruct (char* serialized_pkg, struct package *pkg) {
	if (*serialized_pkg++==STX) {
		char crc=0;
		pkg->subj=(int)*serialized_pkg++;
		pkg->cmd=(int)*serialized_pkg++;
		if (*serialized_pkg++ == calc_crc(pkg->subj, pkg->cmd)) {
			if ((char)*serialized_pkg==ETX) {
				return 0;
			}
		} else return -1;
	} else return -1;
};

void send_pkg(int fd, char* pkg) {
	int count=pkg[1];
	for (int i = 0;i < count+3; i++)
		serialPutchar(fd, pkg[i]);
};