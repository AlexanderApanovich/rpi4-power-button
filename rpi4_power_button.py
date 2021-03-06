import logging
import logging.handlers
import os
import subprocess
import time
from datetime import datetime
import RPi.GPIO as GPIO

# config
gpio_pin = 3
poll_period_sec = 0.1
delay_before_shutdown_sec = 0.5
shutdownCommand = "/sbin/shutdown -h now".split()


def initGPIO():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def initLogging():
    handler = logging.handlers.WatchedFileHandler("/var/log/rpi4_power_button/rpi4_power_button.log")
    formatter = logging.Formatter(logging.BASIC_FORMAT)
    handler.setFormatter(formatter)
    root = logging.getLogger()
    root.setLevel(os.environ.get("LOGLEVEL", "INFO"))
    root.addHandler(handler)


def createLogMessage(message):
    now = datetime.now().strftime("%H:%M:%S")
    return "{now} {message}".format(now=now,message=message)


def logInfo(message):
    logging.info(createLogMessage(message))


def logError(message):
    logging.exception(createLogMessage(message))


def shutdown():
    try:
        logInfo("shutting down...")
        subprocess.call(shutdownCommand, shell=False)
    except Exception as e:
        logError(str(e))


def init():
    initGPIO()
    initLogging()

    while True:
        time.sleep(poll_period_sec)
        if GPIO.input(gpio_pin) == False:
            while GPIO.input(gpio_pin) == False:
                time.sleep(delay_before_shutdown_sec)
            shutdown()


init()
