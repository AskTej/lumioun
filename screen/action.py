def wifi_test(logger):
    logger.info("Running WiFi Test...")

def servo_test(logger):
    logger.info("Running Servo Test...")

def bno_test(logger):
    logger.info("Running BNO055 Test...")

def sim900_test(logger):
    logger.info("Running SIM900 Test...")

def sim900_boot(logger):
    logger.info("Booting SIM900...")

def loc_sim(logger):
    logger.info("Checking SIM location...")

def loc_gps(logger):
    logger.info("Checking GPS location...")

ACTIONS = {
    "WIFITest": wifi_test,
    "ServoTest": servo_test,
    "BNOTest": bno_test,
    "SIM900Test": sim900_test,
    "SIM900 Boot": sim900_boot,
    "LOCSIM": loc_sim,
    "LOCGPS": loc_gps,
}