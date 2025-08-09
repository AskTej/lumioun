from output.servo import Servo

import subprocess
import socket

class ActionManager:    
    def __init__(self, display, logger):        
        self.servo = Servo(logger)
        self.display = display
        self.logger = logger

    def wifi_test(self):
        self.logger.info("[WIFI TEST] Starting")    
        try:
            subprocess.check_call(["ping", "-c", "1", "8.8.8.8"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            connected = True
        except subprocess.CalledProcessError:
            connected = False    
        ip_address = "N/A"
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip_address = s.getsockname()[0]
            s.close()
        except:
            pass

        status_text = "Connected" if connected else "Not Connected"
        self.logger.info(f"[WIFI TEST] Status: {status_text}, IP: {ip_address}")

        if self.display:
            self.display.displayScreen(["WIFI TEST", status_text, f"IP: {ip_address}", "#->Back"])
        self.logger.info("Running WiFi Test...")

    def ServoTest(self):
        if self.servo:
            self.servo.test()