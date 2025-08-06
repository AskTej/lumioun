import time
import RPi.GPIO as GPIO
from utils.logger import get_logger
from input.keypad import KeypadHandler
from output.oled import OLEDDisplay

logger = get_logger()
logger.info("[MAIN] Starting program")

def main():
    logger.info("[MAIN] Starting main function")    
    print("[MAIN] Keypad Init Start")
    myKeypad = KeypadHandler(logger)    
    print("[MAIN] Keypad Init Done")
    time.sleep(1)
    print("[MAIN] OLED Init Start")
    myDisplay = OLEDDisplay(logger)
    print("[MAIN] OLED Init Done")
    time.sleep(1)
    print("[MAIN] Starting main loop")
    myDisplay.displayLines("Lumioun System", 0)
    myDisplay.displayLines("Booting", 2)
    time.sleep(2)
    while True:
        key = myKeypad.get_key()
        if key:
            print("[MAIN] "+key+" pressed.", key)
            if key == '#':
                print("[MAIN] '#' pressed. Exiting loop.")
                break
        time.sleep(0.1)
    myDisplay.clear()

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