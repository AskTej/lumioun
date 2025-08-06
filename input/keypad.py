import time
import RPi.GPIO as GPIO
import threading

class KeypadHandler:
    def __init__(self, logger):
        self.logger = logger
        self.logger.info("[KEYPAD] Starting keypad init")
        GPIO.setmode(GPIO.BCM)            
        GPIO.setwarnings(False)

        self.KEYPAD = [
            ["1","2","3","A"],
            ["4","5","6","B"],
            ["7","8","9","C"],
            ["*","0","#","D"]
        ]

        self.ROW_PINS = [6, 13, 19, 26] # R1 → R4
        self.COL_PINS = [17, 22, 23, 5] # C1 → C4        

        for row in self.ROW_PINS:
            GPIO.setup(row, GPIO.OUT)
            GPIO.output(row, GPIO.LOW)

        for col in self.COL_PINS:
            GPIO.setup(col, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        logger.info("[KEYPAD] Starting keypad init done")

    def get_key(self):
        for i, row_pin in enumerate(self.ROW_PINS):
            GPIO.output(row_pin, GPIO.HIGH)
            for j, col_pin in enumerate(self.COL_PINS):
                if GPIO.input(col_pin) == GPIO.HIGH:
                    time.sleep(0.01)
                    GPIO.output(row_pin, GPIO.LOW)
                    return self.KEYPAD[i][j]
            GPIO.output(row_pin, GPIO.LOW)
        time.sleep(0.05)
        return None