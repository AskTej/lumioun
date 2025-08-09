import pyrebase

class FireManager:
    def __init__(self, logger):
        self.logger = logger
        self.logger.info("[FIRE] Init")

        try:
            # Load Firebase config from lumina.json
            firebase_config = {
                "apiKey": "AIzaSyBvRXUuWR7D21lMK7EvnnRnlJLXL3WZL7E",
                "authDomain": "lumina-9054b.firebaseapp.com",
                "databaseURL": "https://lumina-9054b-default-rtdb.firebaseio.com",
                "projectId": "lumina-9054b",
                "storageBucket": "lumina-9054b.firebasestorage.app",
                "messagingSenderId": "963023421063",
                "appId": "1:963023421063:web:db62b689ceb1519d810222",
                "measurementId": "G-ZH04P6BNBH"
            }

            # Initialize Pyrebase
            firebase = pyrebase.initialize_app(firebase_config)
            self.db = firebase.database()

            self.device_id = "DEV-001"

            # Initial data to push to Realtime DB
            init_data = {
                "deviceid": self.device_id,
                "status": "open",
                "code": "000000",
                "clat": 19.1332352,
                "clon": 72.9350144,
                "dlat": 0,
                "dlon": 0
            }

            # Store in Realtime Database under /devices/DEV-001
            self.db.child("devices").child(self.device_id).set(init_data)

            print(f"[FIREBASE] Initialized device in Realtime DB: {self.device_id}")
        except Exception as e:
            print(f"[FIREBASE] Init failed: {e}")