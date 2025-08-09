import RPi.GPIO as GPIO
import time

class Servo:
    def __init__(self, logger):
        self.logger = logger
        self.pin = 18
        self.logger.info("[SERVO] Initializing on GPIO 18")
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, 50)
        self.pwm.start(0)

    def _rotate(self, duty_cycle, duration=1):
        """Rotate servo to specific duty cycle for given duration"""
        self.pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(duration)
        self.pwm.ChangeDutyCycle(0)

    def open(self):
        """Rotate clockwise"""
        self.logger.info("[SERVO] Opening (Clockwise)")
        self._rotate(7.5)

    def close(self):
        """Rotate anti-clockwise"""
        self.logger.info("[SERVO] Closing (Anti-clockwise)")
        self._rotate(5)

    def test(self):
        """Test servo by rotating both directions"""
        self.logger.info("[SERVO] Test start")
        self.open()
        time.sleep(1)
        self.close()
        time.sleep(1)
        self.logger.info("[SERVO] Test complete")

    def cleanup(self):
        """Release GPIO resources"""
        self.logger.info("[SERVO] Cleaning up GPIO")
        self.pwm.stop()
        GPIO.cleanup()