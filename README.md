# sensorlogger-python
Nextcloud / Owncloud sensorlogger python example script using urllib3
Example for extended data

- calculation of dew point (temperature / humidity required)

## requirements

- Python 3 with urllib3 and Adafruit_DHT installed
- Sensor (e.g. DHT22) connected to Raspberry Pi

## setup

1. Nextcloud: install sensorlogger plugin
2. Nextcloud: generate device password: https://docs.nextcloud.com/server/15/user_manual/session_management.html#managing-devices

3. First edit register.py:
- invent deviceId
- add URL to the sensorlogger api endpoint (__must__ end with __/__)
- nextcloud username and (2.) generated device password
- edit the payload section to match with your configuration (e.g. different data types)
4. Run register.py once (You should see successful response message.)
5. The response message should contain an index for each individual data type you specified (1, 2, 3 - one for each data type)

6. Edit senddata.py:
- same deviceId as in register.py
- url to api endpoint (/createlog/ with __/__ at the end)
- change your sensor type (if != DHT22)
- set your sensor pin to the one the sensor is connected to
- edit payload to match with the description of the data types in register.py and the indices from the response message
- edit username and device passwort

7. Run senddata.py and in your Nextcloud instance you should see the new values being uploaded.
8. To run at startup:
```sudo crontab -e```
Add at the bottom: ```@reboot python3 /path/to/your/script/senddata.py &```
