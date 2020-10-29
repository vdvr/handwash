m32 = atmega32
m32_F = 8000000

nano = atmega328p
nano_F = 16000000

TARGET = main
SRCS = $(TARGET).c ${EXTRA}

EXTRA = uart.c buffer.c conversion.c pkg.c

CFLAGS = -std=c99
CFLAGS += -Wall
CFLAGS += -g
CFLAGS += -Os
CFLAGS += -Wno-misspelled-isr

m32_flags = -p ${m32} -c usbasp -P usb -F
nano_flags = -v -p ${nano} -c arduino -P /dev/cu.wchusbserial14 -b 57600

CC = avr-gcc
OBJCOPY = avr-objcopy
AVRDUDE = avrdude
AVRDUDE_WRITE_FLASH = -U flash:w:${TARGET}.hex:i

compile-nano:
	${CC} ${CFLAGS} -D __UART328p -mmcu=atmega328p -DF_CPU=16000000 -I. -o ${TARGET}.bin ${SRCS}
compile-m32:
	${CC} ${CFLAGS} -D __UART32 -mmcu=atmega32 -DF_CPU=8000000 -I. -o ${TARGET}.bin ${SRCS}
objcpy:
	${OBJCOPY} -j .text -j .data -O ihex ${TARGET}.bin ${TARGET}.hex
m32:
	make clean
	make compile-m32
	make objcpy
	${AVRDUDE} ${m32_flags} ${AVRDUDE_WRITE_FLASH}
nano:
	make clean
	make compile-nano
	make objcpy
	${AVRDUDE} ${nano_flags} ${AVRDUDE_WRITE_FLASH}
clean:
	rm -f *bin *hex
