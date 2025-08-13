import requests
import subprocess
import threading
import time

class LocationManager:
    def __init__(self, db, logger):    
        self.myDb = db
        self.logger = logger
        self.running = True

        self.logger.info("[LOCATION] Init")

        self.thread = threading.Thread(target=self.update_loop, daemon=True)
        self.thread.start()

        self.logger.info("[LOCATION] Background updater started")

    def update_loop(self):        
        while self.running:
            try:
                if self.is_wifi_connected():
                    lat, lon = self.get_wifi_location()
                    self.logger.info(f"[WIFI] Connected. Location: {lat}, {lon}")

                    self.myDb.db.child("devices").child(self.myDb.device_id).update({
                        "wlat": lat,
                        "wlon": lon,
                        "clat": lat,
                        "clon": lon
                    })
                else:
                    lat, lon = 0, 0
                    self.logger.info("[WIFI] Not connected. Location: 0,0")                
            except Exception as e:
                self.logger.error(f"[LOCATION] Error updating: {e}")
            time.sleep(10)
        
    def stop(self):        
        self.running = False
        if self.thread.is_alive():
            self.thread.join(timeout=2)

    @staticmethod
    def is_wifi_connected() -> bool:    
        try:
            subprocess.check_call(
                ["ping", "-c", "1", "-W", "1", "8.8.8.8"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            return True
        except subprocess.CalledProcessError:
            return False
    
    @staticmethod
    def get_wifi_location() -> tuple[float, float]:
        try:
            res = requests.get("https://ipinfo.io/json", timeout=5)
            if res.status_code == 200:
                data = res.json()
                if "loc" in data:
                    lat, lon = data["loc"].split(",")
                    return float(lat), float(lon)
        except Exception:
            pass
        return 0.0, 0.0