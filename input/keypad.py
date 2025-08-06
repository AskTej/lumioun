import time
from pad4pi import rpi_gpio

class KeypadHandler:
    def __init__(self, logger):
        self.logger = logger
        logger.info("[KEYPAD] Starting keypad init")
        KEYPAD = [
            ["1","2","3","A"],
            ["4","5","6","B"],
            ["7","8","9","C"],
            ["*","0","#","D"]
        ]

        ROW_PINS = [6, 13, 19, 26]   # R1 → R4
        COL_PINS = [17, 22, 23, 5]  # C1 → C4

        factory = rpi_gpio.KeypadFactory()
        self.keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)
        logger.info("[KEYPAD] Starting keypad init done")

    def register_callback(self, callback):
        self.keypad.registerKeyPressHandler(callback)

    def cleanup(self):
        self.keypad.cleanup()


