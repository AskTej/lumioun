from screen.action import ACTIONS

class ScreenManager:
    def __init__(self, display, logger):        
        self.display = display
        self.logger = logger
        self.stack = []
        self.page = 0
        self.logger.info("[SCREEN] Init")

        self.menus = {
            "splas": [("", "Lumioun System"), ("", ""), ("", "Booting")],
            "main": [("", "Lumioun System"), ("A", "SYSC"), ("B", "INTL"), ("C", "OPNL"), ("D", "LOCC")],
            "menua": [("#", "Back"), ("A", "WIFITest"), ("B", "ServoTest"), ("C", "BNOTest"), ("D", "Next")],
            "menub": [("#", "Back"), ("A", "SIM900Test"), ("B", "SIM900 Boot"), ("D", "Next")],
            "menuc": [("#", "Back"), ("A", "LOCSIM"), ("B", "LOCGPS")],
        }

        self.current_menu = "splas"
        self.logger.info("[SCREEN] Done")

    def show_screen(self):
        items = self.menus.get(self.current_menu, [])
        lines = [line for _, line in items]
        self.display.displayScreen(lines)

    def change_screen(self, name):
        self.current_menu = name