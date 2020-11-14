#ifndef PERIPHERAL_H_
#define PERIPHERAL_H_

#define true 1

// faucet
#define F_DDR DDRB
#define F_PORT PORTB
#define F_PIN PB0

// soap
#define S_DDR DDRB
#define S_PORT PORTB
#define S_PIN PB1

// faucet sensor
#define F_S_DDR DDRD
#define F_S_PORT PORTD
#define F_S_PORT_PIN PIND
#define F_S_PIN PD2

// soap sensor
#define S_S_DDR DDRD
#define S_S_PORT PORTD
#define S_S_PORT_PIN PIND
#define S_S_PIN PD3

void peripheral_setup(void);
int is_faucet_sensor_set(void);
void faucet_on(void);
void faucet_off(void);
void faucet_on_while_sensor_set(void);
void faucet_on_while_sensor_set_with_timeout(int timeout);

#endif /* PERIPHERAL_H_ */