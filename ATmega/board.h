#ifndef BOARD_H_
#define BOARD_H_

/*
        file for prototype board
        pins used are:
            - PD0 --> RX
            - PD1 --> TX
            - PD2 --> INTO (hardware interupt)
            - PD3 --> INT1
            - PD5 --> led, OC0B
            - PD7 --> led
*/

void boardSetup(void);

void toggleSoap(void);

void toggleWater(void);

#endif /* BOARD_H_ */