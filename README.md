# Topless
Do you drive a Jeep CJ or Wrangler?  Have you ever been caught in a deluge with the top down?   Yeah, we really didn't need to ask that question.   It is a Jeep thing.   We understand.   With this handy device, you will be able to get a quick visual of the weather before you ever leave your house in the morning.

Each super-bright LED represents a 3 hour window.   A green LED means that there is no rain predicted for that time period.   A blue LED means showers are on the way.   An orange LED means it might be a bit too sweltering to drive topless.    And a white LED -- you guessed it -- means that it is going to be freezing cold (or snow is on the way).

Cold blooded?  Don't mind the dry heat?  You can set the temperature thresholds to set your personal preferences in the `config.json` file.

![alt text](https://github.com/eat-sleep-code/topless/blob/master/topless.jpg)

___

## Hardware Requirements
* [Raspberry Pi Zero W](https://www.adafruit.com/product/3400)
* [GPIO Male Headers](https://www.adafruit.com/product/3413)
* [Blinkt! LED](https://www.adafruit.com/product/3195)

___

## Software Requirements
### Configure your Pi ###
* Follow the [installation guide](https://www.raspberrypi.org/downloads/raspbian/) to download and install the latest build of **Raspbian Stretch Lite**.
* Run `sudo raspi-config` and complete the following tasks:
  * Expand file system
  * Setup locale
  * Setup timezone
  * Setup keyboard
  * Set GPU memory to 16MB to allocate most memory to CPU
  * Set up WiFi using this [configuration guide](https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md)
* Run `sudo nano /etc/apt/sources.list`[\*\*](https://www.nano-editor.org/dist/v2.8/nano.html) and uncomment the reference to the source repo 
* Run `sudo apt-get update`
* Run `sudo apt-get dist-upgrade`
* **OPTIONAL:** If using macOS, run the following to allow easy copying of files to your Raspberry Pi: `sudo apt-get install netatalk`
___

### Installing the prerequisites ###
* Install Python and XML libraries
  * Run `sudo apt-get install python3 ipython3 python3-pip python3-rpi.gpio python-dev git`
* Install a few necessary Python packages:
  * Run `sudo pip3 install requests ip2geotools simplejson`
* Setup Blinkt! LED
  * Run `git clone http://github.com/pimoroni/blinkt`
  * Run `cd blinkt/library`
  * Run `sudo python3 setup.py install`
  * Run `cd ~`
___

### Go topless! ###
* Sign up for a free API key at https://home.openweathermap.org/users/sign_up
* Run `git clone https://github.com/eat-sleep-code/topless`
* Run `sudo nano topless/config.json`
* Add your [API key](https://home.openweathermap.org/users/sign_up) and change any other applicable settings
* Run `python topless/topless.py --location [ZIP Code]`   _for example: `python topless/topless.py --location 90210`_
    * Alternatively, you can let the program use geolocation to detect your location: `python topless/topless.py`
___

### Autorun ###
Want to go topless every time you boot your Raspberry Pi?  Here is how!
* Run `sudo nano /etc/systemd/system/topless.service`[\*\*](https://www.nano-editor.org/dist/v2.8/nano.html) and enter the following lines: 
````
[Unit]
Description=Topless service

[Service]
ExecStart=/usr/bin/python3 /home/pi/topless/topless.py --location 90210
Restart=always
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=Topless
User=pi

[Install]
WantedBy=multi-user.target
```
* Run `sudo systemctl enable topless.service`
* Run `sudo systemctl start topless.service`
* Run `sudo reboot`
___


Jeep, the Jeep logo, and the Jeep grille are registered trademarks of FCA US LLC. Throughout this Github repository all the preceding marks and logos are used for identification purposes only. Github and eat-sleep-code are not affiliated with FCA US LLC. Other trademarks used throughout this website are the property of their respective owners and are used for identification purposes only.
