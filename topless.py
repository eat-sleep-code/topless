# Sign up for a free API key at https://home.openweathermap.org/users/sign_up
import argparse
import array
import itertools
import os
import requests
import simplejson as json
import time
from ip2geotools.databases.noncommercial import Freegeoip
from blinkt import set_pixel, set_brightness, show, clear, get_pixel

while True:
    try:
        print("Going topless...")

        # CONFIGURATION
        config = open(os.path.dirname(os.path.abspath(__file__)) + '/config.json').read()
        configJson = json.loads(config)
        apiKey = configJson["apiKey"]    
        thresholdTemperatureLow = float(configJson["thresholds"]["temperature"]["low"])
        thresholdTemperatureHigh = float(configJson["thresholds"]["temperature"]["high"])
        units = configJson["units"].lower().strip()

        # ============================================================================

        parser = argparse.ArgumentParser()
        parser.add_argument('--location', dest="location", help='ZIP Code')
        args = parser.parse_args()

        # base URL
        url = ""
        if (args.location): 
            url =  "https://api.openweathermap.org/data/2.5/forecast?zip=" + args.location
        else:
            currentIP = requests.get("http://ipecho.net/plain?").text
            # print(currentIP)
            currentLocation = Freegeoip.get(currentIP)
            # print(currentLocation)
            url = "https://api.openweathermap.org/data/2.5/forecast?lat=" + str(currentLocation.latitude) + "&lon=" + str(currentLocation.longitude)

        # Metric or Imperial?
        if (units.startswith("m") or units.startswith("c")):
            url = url + "&units=metric"
        else: 
            url = url + "&units=imperial"

        # add API key
        url = url + "&appid=" + apiKey
        #print(url)

        while True: 
            timer = time.time()
            ledEffect = []
            # get forecast
            response = requests.get(url).text 
            clear()

            ledID = 0
            for forecast in (json.loads(response)["list"])[:8]:
                forecastAttributes = json.loads(json.dumps(forecast))
                forecastDate = forecastAttributes["dt_txt"]
                forecastTemp = float(forecastAttributes["main"]["temp"])
                forecastTempMinimum = float(forecastAttributes["main"]["temp_min"])
                forecastTempMaximum = float(forecastAttributes["main"]["temp_max"])
                forecastPressure = float(forecastAttributes["main"]["pressure"]) # hPa
                forecastPressureSeaLevel = float(forecastAttributes["main"]["sea_level"]) # hPa
                forecastPressureGroundLevel = float(forecastAttributes["main"]["grnd_level"]) # hPa
                forecastHumidity = float(forecastAttributes["main"]["humidity"]) # %

                for weather in forecastAttributes["weather"]:
                    forecastWeatherCondition = weather["id"]
                    forecastWeather = weather["main"]
                    forecastWeatherDescription = weather["description"]
                    forecastWeatherIcon = weather["icon"]

                try:
                    forecastClouds = float(forecastAttributes["clouds"]["all"]) # %
                except KeyError:
                    forecastClouds = 0

                try:
                    forecastWindSpeed = float(forecastAttributes["wind"]["speed"])
                    forecastWindDegrees = float(forecastAttributes["wind"]["deg"])
                except KeyError:
                    forecastWindSpeed = 0
                    forecastWindDegrees = 0

                try:
                    forecastRain = float(forecastAttributes["rain"]["3h"]) # mm
                except KeyError:
                    forecastRain = 0

                try:
                    forecastSnow = float(forecastAttributes["snow"]["3h"]) # mm
                except KeyError:
                    forecastSnow = 0

                ledSet = False
                #print(forecastRain)
                if (forecastRain > 3):
                    set_pixel(ledID, 0, 0, 255, 0.6)
                    ledSet = True
                    ledEffect.append('flash')
                elif (forecastRain > 1):
                    set_pixel(ledID, 0, 0, 255, 0.4)
                    ledSet = True
                    ledEffect.append('pulse')
                elif (forecastRain > 0.05):
                    set_pixel(ledID, 0, 0, 128, 0.2)
                    ledSet = True
                    ledEffect.append('none')

                #print(forecastSnow)
                #print(forecastTempMinimum)
                if (forecastSnow > 1 or forecastTempMinimum <= (thresholdTemperatureLow - (thresholdTemperatureLow * 0.20))):
                    set_pixel(ledID, 255, 255, 255, 0.6)
                    ledSet = True
                    ledEffect.append('flash')
                elif (forecastSnow > 1 or forecastTempMinimum <= (thresholdTemperatureLow - (thresholdTemperatureLow * 0.10))):
                    set_pixel(ledID, 255, 255, 255, 0.4)
                    ledSet = True
                    ledEffect.append('pulse')
                elif (forecastSnow > 0.5 or forecastTempMinimum <= thresholdTemperatureLow):
                    set_pixel(ledID, 128, 128, 128, 0.2)
                    ledSet = True
                    ledEffect.append('none')
                
                #print(forecastTempMaximum)
                if (forecastTempMaximum >= (thresholdTemperatureHigh + (thresholdTemperatureHigh * 0.20))):
                    set_pixel(ledID, 255, 128, 0, 0.6)
                    ledSet = True
                    ledEffect.append('flash')
                elif (forecastTempMaximum >= (thresholdTemperatureHigh + (thresholdTemperatureHigh * 0.10))):
                    set_pixel(ledID, 255, 128, 0, 0.4)
                    ledSet = True
                    ledEffect.append('pulse')
                elif (forecastTempMaximum >= thresholdTemperatureHigh):
                    set_pixel(ledID, 255, 180, 0, 0.2)
                    ledSet = True
                    ledEffect.append('none')

                if (ledSet == False):
                    set_pixel(ledID, 0, 128, 0, 0.2)
                    ledSet = True
                    ledEffect.append('none')
            
                show()
                ledID += 1

            while time.time() - timer < 600:
                ledToManipulate = 0
                while ledToManipulate < 8:
                    priorPixelValue = (get_pixel(ledToManipulate))
                    if (ledEffect[ledToManipulate] == 'flash'):
                        for flash in itertools.repeat(None, 6):
                            set_pixel(ledToManipulate, 255, 0, 0, 1.0)
                            show()
                            time.sleep(0.05)
                            set_pixel(ledToManipulate, priorPixelValue[0], priorPixelValue[1], priorPixelValue[2], priorPixelValue[3])
                            show()
                    elif (ledEffect[ledToManipulate] == 'pulse'):
                        for flash in itertools.repeat(None, 4):
                            set_pixel(ledToManipulate, priorPixelValue[0], priorPixelValue[1], priorPixelValue[2], 1.0)
                            show()
                            time.sleep(0.1)
                            set_pixel(ledToManipulate, priorPixelValue[0], priorPixelValue[1], priorPixelValue[2], priorPixelValue[3])
                            show()
                    else:
                        time.sleep(0.05)
                    ledToManipulate += 1
    except:
        print("Please wait...")
    time.sleep(15)




