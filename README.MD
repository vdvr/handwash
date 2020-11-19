# Description
Show hand washing steps on screen for a smart mirror with a Raspberry Pi. An arduino Uno/Nano is used to detect if water or soap is requested and to control if water or soap is allowed. Stable UI releases for the Raspberry Pi are on the raspberry-pi/master branch and stable releases for the Arduino are on the atmega/master branch. 


# Setup
The following steps allow this project to work out-of-the-box on a fresh Raspberry Pi OS install.

## Raspberry Pi
- Clone this repository on the Raspberry Pi: `git clone -b raspberry-pi/master https://github.com/vdvr/handwash`.
- Run the setup file to configure the Raspberry Pi and install the necessary dependencies: `sudo ./setup.sh`.
- Don't reboot yet, or else handwash-worker.service will have to be stopped before programming the Arduino.

## Arduino
- Clone the Arduino branch in a different folder: `git clone -b atmega/master https://github.com/vdvr/handwash`.
- Connect the Arduino to the Raspberry Pi throught USB.
- Program the Arduino Uno/Nano with: `make nano`

- Reboot the Raspberry Pi
- All set!


# Change steps
Changing the hand washing steps can be done very easily in the steps.yaml file. First you can change the welcome text by replacing the text after `startText`. Individual steps can be changed by editing the list items under `steps`. There each step has a description that is showed in the UI `description`, a media file to display `displayPath`, a duration `durationS` and whether the step allows water or soap `water` and `soap` (`False` if property omitted, set to `True` to allow). Steps can be added, changed, removed or reordered, as long as the first step allows water or soap (trigger for UI showing steps to start). Steps without duration will be automatically advanced if the user is done using the water or soap. Media files can be png, bmp, gif, mp4, webm, mov, avi or mpg. For more information on how to use yaml files, please refer to the documentation (https://yaml.org/spec/1.2/spec.html).
If the UI is already running, be sure to restart it to apply changes in steps.yaml: `sudo systemctl restart handwash-ui`.


# Developing
To enable the pipenv virtual environment use: `pipenv shell`.
To add python dependencies use: `pipenv install <pypi package>`.
