import board
import digitalio
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont
import time

class OLEDDisplay:
    def __init__(self, logger):
        self.logger = logger
        self.logger.info("[OLED] OLED Init")        
        self.resetPin = digitalio.DigitalInOut(board.D27)
        self.resetPin.direction = digitalio.Direction.OUTPUT

        self.resetPin.value = False
        time.sleep(0.2)
        self.resetPin.value = True
        time.sleep(0.2)

        self.logger.info("[OLED] OLED Reset Done")        
        spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI)
        dc = digitalio.DigitalInOut(board.D25)
        cs = digitalio.DigitalInOut(board.D8)
        reset = digitalio.DigitalInOut(board.D27)
        self.font = ImageFont.load_default()
        self.display = adafruit_ssd1306.SSD1306_SPI(128, 64, spi, dc, reset, cs)

        self.display.fill(0)
        self.display.show()
        self.logger.info("[OLED] OLED Init Done")

    def displayLines(self, text, index):
        try:
            self.display.fill(0)
            self.display.show()
            image = Image.new("1", (128, 64))
            draw = ImageDraw.Draw(image)        
            draw.text((0, index * 10), text, font=self.font, fill=255)
            self.display.image(image)
            self.display.show()
        except Exception as e:
            self.logger.info(f"[OLED] show_centered failed: {e}")
    
    def clear(self):
        try:
            self.logger.info("[OLED] Cleared and reset")            
            self.resetPin.value = False
            time.sleep(0.2)
            self.resetPin.value = True
            time.sleep(0.2)
            self.display.fill(0)
            time.sleep(0.1)
            self.display.show()
            time.sleep(0.1)
        except Exception as e:
            self.logger.info(f"[OLED] Clear failed: {e}")            