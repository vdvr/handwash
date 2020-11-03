#ifndef __Serial__
#define __Serial__

int serial_open(const char *device);
int serial_get_char(const int fd);
void serial_send_char(const int fd, const unsigned char c);

#endif
