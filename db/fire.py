import pyrebase

class FireManager:
    def __init__(self, logger):
        self.logger = logger
        self.logger.info("[FIRE] Init")

        try:            
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
            
            firebase = pyrebase.initialize_app(firebase_config)
            self.db = firebase.database()

            self.device_id = "DEV-001"

            init_data = {
                "deviceid": self.device_id,
                "status": "open",
                "code": "000000",
                "clat": 0,
                "clon": 0,
                "dlat": 0,
                "dlon": 0
            }
            
            self.db.child("devices").child(self.device_id).set(init_data)
            print(f"[FIREBASE] Initialized device in Realtime DB: {self.device_id}")
        except Exception as e:
            print(f"[FIREBASE] Init failed: {e}")