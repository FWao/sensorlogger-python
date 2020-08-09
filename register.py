#!/usr/bin/python
import sys
import json
import urllib3
import base64
import pprint
import http.client


deviceId = '' # set uuid like d5494cc8-9c52-11ea-bb37-0242ac130002
url = '' # https://CLOUD.MYCLOUD.XYZ/index.php/apps/sensorlogger/api/v1/registerdevice/ -> NOTE: SLASH AT THE END is necessary

def registerDevice():

    # Example extended registration config:

    payload = {
        'deviceId': deviceId,
        'deviceName': 'Sensor#1',
        'deviceType': 'IndoorTempHumid',
        'deviceGroup': 'living room',
        'deviceDataTypes': [
            {
            'type': 'temperature',
            'description': 'Temperatur',
            'unit': '°C'
            },
            {
            'type': 'humidity_rel',
            'description': 'rel. Luftfeuchtigkeit',
            'unit': '% r.F.'
            },
            {
            'type': 'dew_point',
            'description': 'Taupunkt',
            'unit': '°C'
            }
        ]
    }

    encoded_body = json.dumps(payload)

    http = urllib3.PoolManager()

    credentials = '%s:%s' % ('USERNAME', 'DEVICE PASSWORD')
    encoded_credentials = base64.b64encode(credentials.encode('ascii'))

    r = http.request('POST', url, headers={'Content-Type': 'application/json', "Content-Security-Policy" : "default-src 'none';script-src 'self' 'unsafe-eval';style-src 'self' 'unsafe-inline';img-src 'self' data: blob:;font-src 'self';connect-src 'self';media-src 'self'", "Authorization" : "Basic %s" % encoded_credentials.decode('ascii')},
             body=encoded_body)

    print(r.data)


registerDevice()
