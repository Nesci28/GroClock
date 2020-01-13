import RPi.GPIO as GPIO
from datetime import datetime
import time
import json

with open('config.json', 'r') as jsonFile:
    config_vars = jsonFile.read()
    config_vars = json.loads(config_vars)
    red = {
        "GPIO": config_vars['GPIO']['red'],
        "hour": config_vars['time']['red']['hour'],
        "minute": config_vars['time']['red']['minute']
    }
    yellow = {
        "GPIO": config_vars['GPIO']['yellow'],
        "hour": config_vars['time']['yellow']['hour'],
        "minute": config_vars['time']['yellow']['minute']
    }
    green = {
        "GPIO": config_vars['GPIO']['green'],
        "hour": config_vars['time']['green']['hour'],
        "minute": config_vars['time']['green']['minute']
    }

GPIO.setmode(GPIO.BCM)
GPIO.setup([2, 3, 4, 17, 27, 22, 10, 9, 11, 5], GPIO.OUT, initial=GPIO.LOW)

current_led_on = []

while True:
    led_off = red["GPIO"] + yellow["GPIO"] + green["GPIO"]
    now = datetime.now()
    current_hour = int(now.strftime('%H'))
    current_minute = int(now.strftime('%M'))

    if (current_hour > red["hour"] or (current_hour == red["hour"] and current_minute >= red["minute"])) or (current_hour < yellow["hour"] or (current_hour == yellow["hour"] and current_minute < yellow["minute"])):
        time_diff = int(
            24 - red["hour"] + yellow["hour"])
        if current_hour < red["hour"] + time_diff:
            led_on = [5, 11, 9, 10, 22]
        if current_hour >= red["hour"] + time_diff and current_hour < red["hour"] + time_diff * 2:
            led_on = [11, 9, 10, 22]
        if current_hour >= red["hour"] + time_diff * 2 and current_hour < red["hour"] + time_diff * 3:
            led_on = [9, 10, 22]
        if current_hour >= red["hour"] + time_diff * 3 and current_hour < red["hour"] + time_diff * 4:
            led_on = [10, 22]
        if current_hour >= red["hour"] + time_diff * 4 and current_hour < red["hour"] + time_diff * 5:
            led_on = [22]

    elif (current_hour >= yellow["hour"] and current_minute >= yellow["minute"]) and ((current_hour == green["hour"] and current_minute < green["minute"]) or current_hour < green["hour"]):
        total_current_minutes = current_hour * 60 + current_minute
        total_yellow_minutes = yellow["hour"] * 60
        if total_current_minutes < total_yellow_minutes + 15:
            led_on = [27, 17, 4, 3]
        elif total_current_minutes < total_yellow_minutes + 30:
            led_on = [17, 4, 3]
        elif total_current_minutes < total_yellow_minutes + 45:
            led_on = [4, 3]
        elif total_current_minutes < total_yellow_minutes + 60:
            led_on = [3]

    elif (current_hour == green["hour"] and current_minute >= green["minute"]) or current_hour > green["hour"]:
        led_on = [2]

    if current_led_on != led_on:
        current_led_on = led_on
        for led in led_on:
            led_off.remove(led)
        GPIO.output(led_off, 0)
        GPIO.output(led_on, 1)

    time.sleep(15)
