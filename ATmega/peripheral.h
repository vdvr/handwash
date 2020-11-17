#ifndef PERIPHERAL_H_
#define PERIPHERAL_H_

#define true 1

// faucet
#define F_DDR DDRD
#define F_PORT PORTD
#define F_PIN PD5

// soap
#define S_DDR DDRD
#define S_PORT PORTD
#define S_PIN PD7

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

int is_soap_sensor_set(void);
void soap_on(void);
void soap_off(void);
void soap_on_while_sensor_set(void);

#endif /* PERIPHERAL_H_ */