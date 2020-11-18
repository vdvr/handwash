sudo apt install libvlc-dev

# disable screen timeout
sudo tee -a /etc/xdg/lxsession/LXDE-pi/autostart > /dev/null <<EOF
@xset s noblank
@xset s off
@xset -dpms
EOF

sudo echo 'ACTION=="add", SUBSYSTEM=="tty", ATTRS{idVendor}=="2341", ATTRS{idProduct}=="0043", SYMLINK+="arduino"' >> /etc/udev/rules.d/81-arduino.rules
sudo udevadm control --reload-rules && sudo udevadm trigger