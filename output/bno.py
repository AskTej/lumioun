import time
import math
import threading
import board
import busio
import adafruit_bno055

class BNO6652:
    def __init__(self):                
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_bno055.BNO055_I2C(self.i2c)

        self.calibrated = False
        self._calibrate()

        self.logging = False
        self.log_thread = None
        self.current_latlon = (0.0, 0.0)

    def _calibrate(self):        
        print("[INFO] Calibrating BNO055...")
        for _ in range(50):  # ~5 seconds wait
            sys, gyro, accel, mag = self.sensor.calibration_status
            if sys == 3 and gyro == 3 and accel == 3 and mag == 3:
                self.calibrated = True
                print("[INFO] Calibration complete.")
                return
            time.sleep(0.1)
        print("[WARN] Calibration not fully achieved.")
        self.calibrated = False

    def recalibrate(self):        
        self._calibrate()

    def start_logging(self):        
        if self.logging:
            print("[WARN] Already logging.")
            return

        # Get initial GPS location
        lat, lon = self.sim.get_gps_location()
        if lat == 0.0 and lon == 0.0:
            # fallback to LBS if GPS not ready
            lat, lon = self.sim.get_lbs_location()
        self.current_latlon = (lat, lon)

        self.logging = True
        self.log_thread = threading.Thread(target=self._log_loop, daemon=True)
        self.log_thread.start()
        print("[INFO] Logging started from:", self.current_latlon)

    def _log_loop(self):        
        last_time = time.time()
        while self.logging:
            time.sleep(0.2)
            accel = self.sensor.linear_acceleration
            heading = self.sensor.euler[0]  # yaw

            if accel and heading is not None:
                now = time.time()
                dt = now - last_time
                last_time = now

                ax, ay, az = accel
                # simple 2D displacement estimate (very rough!)
                dx = ax * dt * dt / 2
                dy = ay * dt * dt / 2

                # convert displacement to lat/lon delta (~111111 m per degree)
                meters_per_deg = 111111
                dlat = dy / meters_per_deg
                dlon = dx / (meters_per_deg * math.cos(math.radians(self.current_latlon[0])))

                lat = self.current_latlon[0] + dlat
                lon = self.current_latlon[1] + dlon
                self.current_latlon = (lat, lon)

    def get_location(self):        
        return self.current_latlon

    def stop_logging(self):        
        if not self.logging:
            print("[WARN] Logging already stopped.")
            return
        self.logging = False
        if self.log_thread:
            self.log_thread.join(timeout=1)
        print("[INFO] Logging stopped.")