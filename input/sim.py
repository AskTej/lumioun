import serial
import time
import re

class SIM7600:
    def __init__(self, logger, port="/dev/ttyUSB2", baudrate=115200, timeout=1):
        self.logger = logger
        self.logger.info("[SIM] Starting sim init")
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None
        self.connected = False
        self.connect()

    def connect(self):
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            time.sleep(1)
            self.ser.flushInput()
            if self.send_at("AT", "OK", 2):
                self.connected = True
            else:
                self.connected = False
        except Exception as e:
            print(f"[ERROR] Could not connect: {e}")
            self.connected = False

    def send_at(self, command, expected, timeout=2):
        if not self.ser:
            return False
        self.ser.write((command + "\r\n").encode())
        time.sleep(timeout)
        reply = self.ser.read_all().decode(errors="ignore")
        return expected in reply, reply

    def get_gps_location(self):
        ok, reply = self._send_at("AT+CGPSINFO", "+CGPSINFO:", 2)
        if ok and "+CGPSINFO:" in reply:
            data = reply.split("+CGPSINFO:")[1].split("\r\n")[0].strip()
            if data and "," in data:
                parts = data.split(",")
                if len(parts) >= 4 and parts[0] and parts[2]:
                    lat = self.convert_to_decimal(parts[0], parts[1])
                    lon = self.convert_to_decimal(parts[2], parts[3])
                    return (lat, lon)
        return (0.0, 0.0)

    def convert_to_decimal(self, raw, direction):
        try:
            raw = float(raw)
            deg = int(raw / 100)
            minutes = raw - deg * 100
            decimal = deg + minutes / 60
            if direction in ["S", "W"]:
                decimal = -decimal
            return decimal
        except:
            return 0.0

    def check_sim_status(self):
        status = {"sim_present": False, "network": "Unknown"}
        ok, reply = self.send_at("AT+CPIN?", "READY", 2)
        if ok:
            status["sim_present"] = True
        ok, reply = self.send_at("AT+CREG?", "+CREG:", 2)
        if ok:
            if ",1" in reply or ",5" in reply:
                status["network"] = "Registered"
            else:
                status["network"] = "Not Registered"
        return status

    def get_lbs_location(self):
        ok, reply = self.send_at("AT+CIPGSMLOC=1,1", "+CIPGSMLOC:", 5)
        if ok and "+CIPGSMLOC:" in reply:
            try:
                line = reply.split("+CIPGSMLOC:")[1].split("\r\n")[0].strip()
                parts = line.split(",")
                if len(parts) >= 3 and parts[1] and parts[2]:
                    lat = float(parts[1])
                    lon = float(parts[2])
                    return (lat, lon)
            except:
                pass
        return (0.0, 0.0)