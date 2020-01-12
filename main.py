import RPi.GPIO as GPIO
from datetime import datetime
import time

# 2 = Green
# 3 = 4th Yellow
# 4 = 3rd Yellow
# 17 = 2sd Yellow 
# 27 = 1st Yellow
# 22 = 5th Red
# 10 = 4th Red
# 9 = 3rd Red
# 11 = 2sc Red
# 5 = 1st Red

GPIO.setmode(GPIO.BCM)
GPIO.setup([2, 3, 4, 17, 27, 22, 10, 9, 11, 5], GPIO.OUT, initial=GPIO.LOW)

current_led_on = []

while True:
    red = {
        "hour": 20,
        "minute": 0
    }
    yellow = {
        "hour": 6,
        "minute": 0
    }
    green = {
        "hour": 7,
        "minute": 0
    }
    led_off = [2, 3, 4, 17, 27, 22, 10, 9, 11, 5]

    now = datetime.now()
    current_hour = int(now.strftime('%H'))
    current_minute = int(now.strftime('%M'))

    if (current_hour > red["hour"] or (current_hour == red["hour"] and current_minute >= red["minute"])) or (current_hour < yellow["hour"] or (current_hour == yellow["hour"] and current_minute < yellow["minute"])):
        if current_hour < red["hour"] + 2:
            led_on = [5, 11, 9, 10, 22]
        if current_hour >= red["hour"] + 2 and current_hour < red["hour"] + 4:
            led_on = [11, 9, 10, 22]
        if current_hour >= red["hour"] + 4 and current_hour < red["hour"] + 6:
            led_on = [9, 10, 22]
        if current_hour >= red["hour"] + 6 and current_hour < red["hour"] + 8:
            led_on = [10, 22]
        if current_hour >= red["hour"] + 8 and current_hour < red["hour"] + 10:
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


    global current_led_on
    if current_led_on != led_on:
        current_led_on = led_on
        for led in led_on:
            led_off.remove(led)
        GPIO.output(led_off, 0)
        GPIO.output(led_on, 1)

    time.sleep(15)