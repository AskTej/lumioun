from typing import Literal
from screen.action import ActionManager
from db.fire import FireManager

class ScreenManager:
    def __init__(self, display, logger):        
        self.display = display
        self.logger = logger
        self.stack = []
        self.page = 0
        self.actions = ActionManager(display, logger)
        self.myDb = FireManager(logger)
        self.logger.info("[SCREEN] Init")

        self.input_mode = None
        self.entered_code = ""

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

    def goto_main(self):
        self.stack = []
        self.current_menu = "main"
        self.page = 0
        self.show_screen()        

    def handle_input(self, key):
        if self.input_mode in ['INTL', 'OPNL']:            
            if key.isdigit():
                self.entered_code += key
                self.display.displayScreen([
                    f"{self.input_mode} MODE",
                    "Enter Code:",
                    "*" * len(self.entered_code)
                ])

                if len(self.entered_code) == 6:
                    if self.input_mode == 'INTL':
                        self.finalize_intl()
                    elif self.input_mode == 'OPNL':
                        self.finalize_opnl()
            elif key == "#":
                self.reset_input_mode()
        else:
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

            elif label == "D->Next" or label == "Next":            
                sysc_pages = ["A->SYSC", "menub", "menuc"]
                if self.current_menu in sysc_pages:
                    idx = sysc_pages.index(self.current_menu)
                    next_idx = (idx + 1) % len(sysc_pages)
                    self.stack.append(self.current_menu)
                    self.current_menu = sysc_pages[next_idx]
                    self.page = 0
                    self.show_screen()
                else:
                    self.logger.info("[SCREEN] No next page for this menu")

            elif label in self.menus:
                if label == "B->INTL" or label == "C->OPNL":
                    match label:
                        case "B->INTL":
                            self.start_intl()
                        case "C->OPNL":
                            self.start_opnl()
                else:
                    self.change_screen(label)

            else:            
                match label:
                    case "A->WIFITest":
                        self.actions.wifi_test()
                    case "B->ServoTest":
                        self.actions.ServoTest()
                    case "# -> Back to Menu":
                        self.goto_main()
                    case _:
                        self.logger.warning(f"[SCREEN] Unknown label: {label}")

    
    def start_intl(self):
        self.logger.info("[INTL] Start - Waiting for code input")
        self.input_mode = 'INTL'
        self.entered_code = ""
        self.display.displayScreen(["INTL MODE", "Enter 6-digit code:"])

    def start_opnl(self):
        self.logger.info("[OPNL] Start - Waiting for code input")
        self.input_mode = 'OPNL'
        self.entered_code = ""
        self.display.displayScreen(["OPNL MODE", "Enter 6-digit code:"])

    def finalize_intl(self):
        code = self.entered_code
        self.logger.info(f"[INTL] Code set to {code}")
        self.myDb.db.child("devices").child(self.myDb.device_id).update({
            "status": "closed",
            "code": code
        })
        self.display.displayScreen(["Lock Init Done"])
        self.reset_input_mode()

    def finalize_opnl(self):
        doc = self.myDb.get_document()
        if doc and doc.get("code") == self.entered_code:
            self.logger.info("[OPNL] Code matched, unlocking")
            self.myDb.db.child("devices").child(self.myDb.device_id).update({
                "status": "open",
                "code": "000000"
            })
            self.display.displayScreen(["Lock Opened"])
        else:
            self.logger.warning("[OPNL] Wrong code")
            self.display.displayScreen(["Wrong Code"])
        self.reset_input_mode()

    def reset_input_mode(self):
        self.input_mode = None
        self.entered_code: Literal[''] = ""
        self.display.displayScreen(["# -> Back to Menu"])