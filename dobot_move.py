# dobot_move.py
from pydobot import Dobot

class DobotController:
    def __init__(self, port="/dev/ttyUSB0"):  # ปรับตามของคุณ
        self.dobot = Dobot(port=port)
        # กำหนดตำแหน่ง
        self.positions = {
            "Home": (200, 0, 50),
            "Block1_start": (200, 50, 50),
            "Block1_finish": (300, 50, 50),
            "Block2_start": (200, 150, 50),
            "Block2_finish": (300, 150, 50),
        }
        self.dobot.move_to(*self.positions["Home"])  # เริ่มจาก Home

    def act_on_label(self, label):
        """ขยับกล่องตามตัวอักษร"""
        if label in "ABCDEFGHIJKLMNOP":
            start = self.positions["Block1_start"]
            finish = self.positions["Block1_finish"]
        elif label in "QRSTUVWXYY":
            start = self.positions["Block2_start"]
            finish = self.positions["Block2_finish"]
        else:
            return  # ตัวอักษรอื่นไม่ทำอะไร

        # ขยับกล่อง: ไป Start -> Finish -> Home
        self.dobot.move_to(*start)
        self.dobot.move_to(*finish)
        self.dobot.move_to(*self.positions["Home"])

    def close(self):
        self.dobot.close()
