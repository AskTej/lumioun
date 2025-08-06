import firebase_admin
from firebase_admin import credentials, firestore
import os

class FireManager:
    def __init__(self, logger):        
        self.logger = logger
        self.logger.info("[FIRE] Init")        
        try:
            base_path = os.path.dirname(os.path.abspath(__file__))
            key_path = os.path.join(base_path, "lumina.json")
            cred = credentials.Certificate(key_path)
            firebase_admin.initialize_app(cred)
            self.db = firestore.client()
            self.device_id = "DEV-001"
            doc_ref = self.db.collection("devices").document(self.device_id)
            init_data = {
                "deviceid": self.device_id,
                "status": "open",
                "code": "000000",
                "clat": 19.1332352,
                "clon": 72.9350144,
                "dlat": 0,
                "dlon": 0
            }
            doc_ref.set(init_data)
            print(f"[FIREBASE] Initialized device doc: {self.device_id}")
        except Exception as e:
            print(f"[FIREBASE] Init failed: {e}")