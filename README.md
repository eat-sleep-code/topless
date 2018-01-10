# Topless

## Hardware Requirements
* [Raspberry Pi Zero W](https://www.adafruit.com/product/3400)
* [GPIO Male Headers](https://www.adafruit.com/product/3413)
* [Blinkt! LED] https://www.adafruit.com/product/3195

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
  * Run `sudo apt-get install python3 ipython3 python3-pip python3-rpi.gpio libxml2-dev libxslt-dev python-dev python3-lxml`
  * Run `sudo apt-get build-dep python3-lxml`
* Install the LXML and Natural packages:
  * Run `sudo pip3 install lxml`
  * Run `sudo pip3 install natural`
  * Run `sudo pip3 install ip2geotools`
  * Run `sudo pip3 install simplejson`
* Setup Blinkt! LED
  * Run `curl https://get.pimoroni.com/blinkt | sudo bash`

___
