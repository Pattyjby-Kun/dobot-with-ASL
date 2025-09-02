import cv2
import mediapipe as mp
import joblib
import pandas as pd
import simpleaudio as sa  # <-- ใช้เล่นเสียงแบบไม่บล็อก
from collections import deque
from feature_engineering import extract_features
import os

# โหลดโมเดล
clf = joblib.load("asl_model.pkl")

# โหลดเสียงทั้งหมดล่วงหน้า
sound_folder = "sounds"
sounds = {f.split(".")[0]: sa.WaveObject.from_wave_file(os.path.join(sound_folder, f))
          for f in os.listdir(sound_folder) if f.endswith(".wav")}

# MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

# smoothing buffer
buffer_size = 5
pred_buffer = deque(maxlen=buffer_size)
last_spoken = None

with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                row = {f"{axis}{i}": getattr(lm, axis) for i, lm in enumerate(hand_landmarks.landmark) for axis in ['x','y','z']}
                features = extract_features(row)
                X = pd.DataFrame([features])
                pred = clf.predict(X)[0]

                # เพิ่ม prediction เข้า buffer
                pred_buffer.append(pred)

                # most common prediction
                most_common_pred = max(set(pred_buffer), key=pred_buffer.count)

                # เล่นเสียงถ้าเปลี่ยนตัวอักษร
                if most_common_pred != last_spoken:
                    if most_common_pred in sounds:
                        sounds[most_common_pred].play()  # เล่นแบบไม่บล็อก
                    last_spoken = most_common_pred

                cv2.putText(frame, f"Pred: {most_common_pred}", (50, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)

        cv2.imshow("ASL Recognition", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
