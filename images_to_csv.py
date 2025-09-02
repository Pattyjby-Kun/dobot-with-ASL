import os
import cv2
import mediapipe as mp
import pandas as pd

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1)
data = []

# โฟลเดอร์ dataset (แก้ path ตรงนี้)
dataset_path = r"C:\Users\User\Downloads\archive (1)\SigNN Character Database"

for label in os.listdir(dataset_path):  # เช่น A, B, C, ...
    label_folder = os.path.join(dataset_path, label)
    if not os.path.isdir(label_folder):
        continue
    
    for img_name in os.listdir(label_folder):
        img_path = os.path.join(label_folder, img_name)
        image = cv2.imread(img_path)
        if image is None:
            continue

        # แปลงเป็น RGB
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        if results.multi_hand_landmarks:
            row = {}
            hand_landmarks = results.multi_hand_landmarks[0]

            for i, lm in enumerate(hand_landmarks.landmark):
                row[f"x{i}"] = lm.x
                row[f"y{i}"] = lm.y
                row[f"z{i}"] = lm.z

            row["label"] = label
            data.append(row)

# แปลงเป็น DataFrame และบันทึกเป็น CSV
df = pd.DataFrame(data)
df.to_csv("asl_data.csv", index=False)

print("✅ Dataset saved as asl_data.csv")
