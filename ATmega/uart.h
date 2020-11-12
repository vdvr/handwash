#ifdef __UART32

#define _USART_REGISTER UBRRL
#define _USART_UCSRA UCSRA
#define _USART_UCSRB UCSRB
#define _USART_UCSRC UCSRC
#define _USART_UDRE UDR
#define _USART_UCSZ0 UCSZ0
#define _TXEN TXEN
#define _RXEN RXEN
#define _RXCIE RXCIE
#endif

#ifdef __UART328p

#define _USART_REGISTER UBRR0
#define _USART_UCSRA UCSR0A
#define _USART_UCSRB UCSR0B
#define _USART_UCSRC UCSR0C
#define _USART_UDR0 UDR0
#define _USART_UDRE UDRE0
#define _USART_UCSZ0 UCSZ00
#define _TXEN TXEN0
#define _RXEN RXEN0
#define _RXCIE RXCIE0
#endif 

#ifndef _UART_
#define _UART_

#define BAUDRATE 57600

void uartSetup(long baudrate);
void uartPutChar(char data);
void uartPutASCII(unsigned int data);

#endif /* UARTNANO_H_ */
