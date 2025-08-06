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
            "main": [("", "Lumioun System"), ("A", "A->SYSC"), ("B", "B->INTL"), ("C", "C->OPNL"), ("D", "D->LOCC")],
            "A->SYSC": [("#", "#->Back"), ("A", "A->WIFITest"), ("B", "B->ServoTest"), ("C", "C->BNOTest"), ("D", "D->Next")],
            "menub": [("#", "#->Back"), ("A", "A->SIM900Test"), ("B", "B->SIM900 Boot"), ("D", "D->Next")],
            "menuc": [("#", "#->Back"), ("A", "A->LOCSIM"), ("B", "B->LOCGPS")],
            "B->INTL": [("", "Lumioun System"), ("", "SETUP LOCK"), ("", "Enter Digit"), ("", "------"), ("", ""),("#", "#->Back")],
            "C->OPNL": [("", "Lumioun System"), ("", "OPEN LOCK"), ("", "Enter Digit"), ("", "------"), ("", ""),("#", "#->Back")],
            "D->LOCC": [("#", "#->Back"), ("A", "A->WIFI Loc"), ("B", "B->SIM900 Loc"), ("C", "C->BNO Loc")],
        }

        self.current_menu = "splas"
        self.logger.info("[SCREEN] Done")

    def show_screen(self):
        items = self.menus.get(self.current_menu, [])
        lines = [line for _, line in items]
        self.display.displayScreen(lines)

    def main_screen(self):
        self.current_menu = "main"
        self.page = 0
        self.show_screen()

    def change_screen(self, name):
        if name in self.menus:
            self.stack.append(self.current_menu)
            self.current_menu = name
            self.page = 0
            self.show_screen()
        else:
            self.logger.warning(f"[SCREEN] Unknown screen: {name}")

    def go_back(self):
        if self.stack:
            self.current_menu = self.stack.pop()
            self.page = 0
            self.show_screen()
        else:
            self.logger.info("[SCREEN] Already at root menu")

    def handle_input(self, key):
        key = key.upper()
        menu_items = self.menus.get(self.current_menu, [])
        key_map = dict(menu_items)

        if key not in key_map:
            self.logger.info(f"[SCREEN] Invalid key: {key}")
            return
        
        label = key_map[key]
        self.logger.info(f"[SCREEN] Key {key} → {label}")

        if key == "#":
            self.go_back()
        elif label == "Next":
            self.logger.info("[SCREEN] Next page not implemented")
        elif label in self.menus:
            self.change_screen(label)
        elif label in ACTIONS:
            self.logger.info(f"[SCREEN] Executing action: {label}")
            try:
                ACTIONS[label]()
            except Exception as e:
                self.logger.error(f"[SCREEN] Action failed: {e}")
        else:
            self.logger.warning(f"[SCREEN] Unknown label: {label}")        