#ifndef UART_H_
#define UART_H_

#define F_CPU 16000000

void uartSetup(long baudrate);

void uartPutChar(char data);

#endif /* UART_H_ */