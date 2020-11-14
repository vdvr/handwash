# creates 2 linked pseudoterminals which can be used for serial communication
# will print the 2 devices in the form  "/dev/pts/x" when ran
# keep script running aslong as linked PTYs are needed
#!/bin/bash

dpkg -s socat &> /dev/null

if [ $? -ne 0 ]
then
    sudo apt update && sudo apt install socat
fi

socat -d -d pty,raw,echo=0 pty,raw,echo=0