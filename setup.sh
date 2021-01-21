# disable screen timeout
sudo tee -a /etc/xdg/lxsession/LXDE-pi/autostart > /dev/null <<EOF
@xset s noblank
@xset s off
@xset -dpms
EOF

# disable usb handshaking
sudo echo 'ACTION=="add", SUBSYSTEM=="tty", ATTRS{idVendor}=="2341", ATTRS{idProduct}=="0043", SYMLINK+="arduino"' >> /etc/udev/rules.d/81-arduino.rules
sudo udevadm control --reload-rules && sudo udevadm trigger

make -C rpicom all
sudo ln -s $(pwd) /usr/share/handwash

#enable picam
sudo tee -a /boot/config.txt > /dev/null <<EOF
start_x=1
gpu_mem=128
EOF

# create systemd services
sudo tee /etc/systemd/system/handwash-ui.service > /dev/null <<EOF
[Unit]
Description=handwash GUI service
After=graphical.target
StartLimitIntervalSec=0
[Service]
Environment="DISPLAY=:0"
WorkingDirectory=/usr/share/handwash
Type=simple
Restart=always
RestartSec=1
User=pi
ExecStart=python3 /usr/share/handwash/main.py

[Install]
WantedBy=multi-user.target
EOF

sudo tee /etc/systemd/system/handwash-worker.service > /dev/null <<EOF
[Unit]
Description=handwash worker service
After=multi-user.target
StartLimitIntervalSec=0
[Service]
WorkingDirectory=/usr/share/handwash
Type=simple
Restart=always
RestartSec=1
User=root
ExecStart=/usr/share/handwash/rpicom/worker

[Install]
WantedBy=multi-user.target
EOF

# install dependencies
sudo apt update
sudo apt install -y libvlc-dev python3 python3-pyqt5 python3-pyqt5.qtsvg
sudo apt install -y gcc-avr binutils-avr gdb-avr avr-libc avrdude
sudo apt install -y libatlas-base-dev libhdf5-dev libhdf5-serial-dev libatlas-base-dev libjasper-dev  libqtgui4  libqt4-test

# enable systemd services
sudo systemctl enable handwash-worker.service
sudo systemctl enable handwash-ui.service

echo "Please reboot now"