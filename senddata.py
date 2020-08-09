#!/usr/bin/python
import sys
import time
import Adafruit_DHT
import threading
import json
import urllib3
import base64
import pprint
from datetime import datetime
import http.client
import math


interval = 30 # set interval in seconds
deviceId = '' # same as in register.py
url = '' # https://CLOUD.MYCLOUD.XYZ/index.php/apps/sensorlogger/api/v1/createlog/ -> NOTE: SLASH AT THE END is necessary
headers = {'content-type': 'application/json'}

# Which sensor do you want to use?
sensor = Adafruit_DHT.DHT22
pin = 4 # Sensor data pin

def sendData():
    threading.Timer(interval, sensorData).start()
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    cdatetime = datetime.now()
    currentDate = cdatetime.strftime('%Y-%m-%d %H:%M:%S')

    # calculate dew point:
    A = 17.68
    B = 243.12
    tmp = ((A * temperature) / (B + temperature)) + math.log(humidity / 100.0)
    dew_point = (B * tmp) / (A - tmp)

    if humidity is not None and temperature is not None:

        # specify the data to be sent (index 1,2,3 refers to the response in register.py)
        payload = {
                'deviceId': deviceId,
                'date': currentDate,
                'data': [{'dataTypeId':1,
                'value' : temperature},
                {'dataTypeId':2,
                'value' : humidity},
                {'dataTypeId':3,
                'value' : dew_point}]
        }

        encoded_body = json.dumps(payload)

        http = urllib3.PoolManager()

        credentials = '%s:%s' % ('USERNAME', 'DEVICE PASSWORD')
        encoded_credentials = base64.b64encode(credentials.encode('ascii'))

        r = http.request('POST', url, headers={'Content-Type': 'application/json', "Content-Security-Policy" : "default-src 'none';script-src 'self' 'unsafe-eval';style-src 'self' 'unsafe-inline';img-src 'self' data: blob:;font-src 'self';connect-src 'self';media-src 'self'", "Authorization" : "Basic %s" % encoded_credentials.decode('ascii')},
                 body=encoded_body)

        # uncomment to print response (debug)
        # print(r.data)

    else:
        print('Something went wrong with your sensor!')
        sys.exit(1)

sendData()
