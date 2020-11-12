#ifndef TIMER2MIN_H_
#define TIMER2MIN_H_

#define TIMER_OF_1HZ 31249

struct timestamp {
    unsigned int seconds;
    unsigned int extra;
};

extern unsigned int seconds_now;

void timerSetup(void);

void stopTimer(void);

void startTimer(void);

void resetTimer(void);

struct timestamp getTime();

int checkTimeElapsed(struct timestamp time, unsigned int seconds, unsigned int extra);

#endif /* TIMER2MIN_H_ */