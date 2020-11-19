sudo echo 'ACTION=="add", SUBSYSTEM=="tty", ATTRS{idVendor}=="2341", ATTRS{idProduct}=="0043", SYMLINK+="arduino"' >> /etc/udev/rules.d/81-arduino.rules
sudo udevadm control --reload-rules && sudo udevadm trigger

make -C rpicom all