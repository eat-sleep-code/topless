# Topless
Do you drive a Jeep CJ or Wrangler?  Have you ever been caught in a deluge with the top down?   Yeah, we really didn't need to ask that question.   It is a Jeep thing.   We understand.   With this handy device, you will be able to get a quick visual of the weather before you ever leave your house in the morning.

Each LED represents a 3 hour window.   A green LED means that there is no rain predicted for that time period.   A blue LED means showers are on the way.   An orange LED means it might be a bit too sweltering to drive topless.    And a white LED -- you guessed it -- means that it is going to be freezing cold (or snow is on the way).

Cold blooded?  Don't mind the dry heat?  You can set the temperature thresholds to set your personal preferences in the `config.json` file.

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
* Add our API key and change any other applicable settings
* Run `python topless/topless.py --location [ZIP Code]`   _for example: `python topless/topless.py --location 90210`_
    * Alternatively, you can let the program use geolocation to detect your location: `python topless/topless.py`
___

### Autorun ###
Want to go topless every time you boot your Raspberry Pi?  Here is how!
* Run `sudo crontab -e`
* Select `nano`[\*\*](https://www.nano-editor.org/dist/v2.8/nano.html)
* Scroll to the bottom of the file and add these two lines:
    * `@reboot sudo python topless/topless.py --location 90210 &`
    * `0 1 * * * sudo python topless/topless.py --location 90210 &`
___
