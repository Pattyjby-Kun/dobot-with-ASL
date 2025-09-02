import pyttsx3
import os

os.makedirs("sounds", exist_ok=True)

engine = pyttsx3.init('sapi5')  # Windows
engine.setProperty('rate', 150)

for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
    filename = f"sounds/{letter}.wav"
    engine.save_to_file(letter, filename)

engine.runAndWait()
print("สร้างไฟล์เสียงเรียบร้อยแล้ว!")
