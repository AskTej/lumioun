import time
import RPi.GPIO as GPIO
from pad4pi import rpi_gpio
from utils.logger import get_logger
from input.keypad import KeypadHandler

logger = get_logger()
logger.info("[MAIN] Starting program")

def key_handler(key):
    global pressed_key
    print(f"[KEYPAD] You pressed: {key}")
    pressed_key = key

def main():
    logger.info("[MAIN] Starting main function")
    GPIO.setmode(GPIO.BCM)
    print("[MAIN] Keypad Init Start")
    myKeypad = KeypadHandler(logger)
    myKeypad.register_callback(key_handler)
    print("[MAIN] Keypad Init Done")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("[MAIN] Exiting on Ctrl+C")
    except Exception as e:
        logger.info(f"[MAIN] Fatal error: {e}")
    finally:
        try:
            GPIO.cleanup()
            logger.info("[MAIN] GPIO cleaned up")
        except:
            pass