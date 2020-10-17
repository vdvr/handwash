#ifndef UARTNANO_H_
#define UARTNANO_H_

#define F_CPU 16000000

void uartSetup(long baudrate);

void uartPutChar(char data);

#endif /* UARTNANO_H_ */