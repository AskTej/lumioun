import RPi.GPIO as GPIO
import time

TEST_PIN = 5  # One of the keypad's column pins

GPIO.setmode(GPIO.BCM)
GPIO.setup(TEST_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def callback(channel):
    print("Edge detected on GPIO", channel)

GPIO.add_event_detect(TEST_PIN, GPIO.FALLING, callback=callback, bouncetime=300)

try:
    print("Press key connected to GPIO 5...")
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()