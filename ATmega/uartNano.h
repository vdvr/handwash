#ifndef UARTNANO_H_
#define UARTNANO_H_

#define F_CPU 16000000

void uartSetup(long baudrate);

void uartPutChar(char data);

void uartPutASCII(int data);

#endif /* UARTNANO_H_ */