import time
import RPi.GPIO as GPIO
from pad4pi import rpi_gpio
from utils.logger import get_logger

logger = get_logger()
logger.info("[MAIN] Starting program")

def main():
    logger.info("[MAIN] Starting main function")

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