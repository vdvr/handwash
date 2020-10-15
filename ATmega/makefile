#===== Main Options ===========

MCU = atmega32
F_CPU = 8000000

TARGET = main
SRCS = $(TARGET).c ${EXTRA}

EXTRA = board.c

#===== Compile Options ===========

CFLAGS = -std=c99
CFLAGS += -Wall
CFLAGS += -g
CFLAGS += -Os
CFLAGS += -mmcu=${MCU}
CFLAGS += -DF_CPU=${F_CPU} -I.

#===== Programming Options =========

AVRDUDE_PROGRAMMER = usbasp
AVRDUDE_PORT = usb

AVRDUDE_FLAGS = -p ${MCU} -c $(AVRDUDE_PROGRAMMER) -P $(AVRDUDE_PORT) -F

#===== Targets =========

CC = avr-gcc
OBJCOPY = avr-objcopy
AVRDUDE = avrdude

AVRDUDE_WRITE_FLASH = -U flash:w:${TARGET}.hex:i


all:
	${CC} ${CFLAGS} -o ${TARGET}.bin ${SRCS}
	${OBJCOPY} -j .text -j .data -O ihex ${TARGET}.bin ${TARGET}.hex

flash:
	${AVRDUDE} ${AVRDUDE_FLAGS} ${AVRDUDE_WRITE_FLASH}

clean:
	rm -f *bin *hex


help:
	@echo 'Basic targets:'
	@echo '  clean       Remove files created by make.'
	@echo
	@echo 'Flashing:'
	@echo '  flash       Write only flash.'