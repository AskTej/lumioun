import time
import RPi.GPIO as GPIO
import threading

class KeypadHandler:
    def __init__(self, logger):
        self.logger = logger
        self.logger.info("[KEYPAD] Starting keypad init")
        self.KEYPAD = [
            ["1","2","3","A"],
            ["4","5","6","B"],
            ["7","8","9","C"],
            ["*","0","#","D"]
        ]

        self.ROW_PINS = [6, 13, 19, 26] # R1 → R4
        self.COL_PINS = [17, 22, 23, 5] # C1 → C4

        self.lock = threading.Lock()
        self.callback = None

        GPIO.setmode(GPIO.BCM)            
        GPIO.setwarnings(False)

        for row in self.ROW_PINS:
            GPIO.setup(row, GPIO.OUT)
            GPIO.output(row, GPIO.LOW)

        for col in self.COL_PINS:
            GPIO.setup(col, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(col, GPIO.FALLING, callback=self._col_callback, bouncetime=200)
        logger.info("[KEYPAD] Starting keypad init done")

    def _col_callback(self, channel):        
        for row_index, row_pin in enumerate(self.ROW_PINS):
            GPIO.output(row_pin, GPIO.HIGH)
            time.sleep(0.002)
            if GPIO.input(channel) == GPIO.LOW:
                col_index = self.COL_PINS.index(channel)
                key = self.KEYPAD[row_index][col_index]
                self.logger.info(f"[KEYPAD] Key detected: {key}")
                if self.callback:
                    self.callback(key)
                break
            GPIO.output(row_pin, GPIO.LOW)

    def register_callback(self, callback_func):        
        self.callback = callback_func
        self.logger.info("[KEYPAD] Callback registered")

    def cleanup(self):        
        GPIO.cleanup()
        self.logger.info("[KEYPAD] GPIO cleanup complete")