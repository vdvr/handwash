# disable screen timeout
sudo tee -a /etc/xdg/lxsession/LXDE-pi/autostart > /dev/null <<EOF
@xset s noblank
@xset s off
@xset -dpms
EOF

sudo echo 'ACTION=="add", SUBSYSTEM=="tty", ATTRS{idVendor}=="2341", ATTRS{idProduct}=="0043", SYMLINK+="arduino"' >> /etc/udev/rules.d/81-arduino.rules
sudo udevadm control --reload-rules && sudo udevadm trigger

make -C rpicom all

sudo apt update
sudo apt install libvlc-dev python3 python3-pyqt5 python3-pyqt5.qtsvg
