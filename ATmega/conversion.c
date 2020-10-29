#include <avr/io.h>
#include "uart.h"
#include "conversion.h"

char ASCIItoChar (char ASCII)
{
    ASCII -= '0';
    return ASCII;
}
