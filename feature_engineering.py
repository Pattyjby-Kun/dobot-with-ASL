# feature_engineering.py
import numpy as np
import pandas as pd

def calculate_distance(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

def calculate_angle(v1, v2):
    """ คำนวณมุมระหว่างเวกเตอร์สองตัว """
    v1, v2 = np.array(v1), np.array(v2)
    cos_theta = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-9)
    return np.arccos(np.clip(cos_theta, -1.0, 1.0))

def extract_features(row):
    features = {}
    points = [(row[f"x{i}"], row[f"y{i}"], row[f"z{i}"]) for i in range(21)]

    # ตัวอย่าง: ระยะระหว่างนิ้วคู่หลัก
    features["dist_thumb_index"] = calculate_distance(points[4], points[8])
    features["dist_index_middle"] = calculate_distance(points[8], points[12])
    features["dist_middle_ring"] = calculate_distance(points[12], points[16])
    features["dist_ring_pinky"] = calculate_distance(points[16], points[20])
    
    # มุมระหว่างนิ้ว
    v_thumb_index = np.array(points[8]) - np.array(points[4])
    v_index_middle = np.array(points[12]) - np.array(points[8])
    features["angle_thumb_index_middle"] = calculate_angle(v_thumb_index, v_index_middle)

    # wrist vs fingertips
    for i, name in zip([4,8,12,16,20], ["thumb","index","middle","ring","pinky"]):
        features[f"diff_wrist_{name}_x"] = points[0][0] - points[i][0]
        features[f"diff_wrist_{name}_y"] = points[0][1] - points[i][1]
        features[f"diff_wrist_{name}_z"] = points[0][2] - points[i][2]

    return features

def create_feature_set(data):
    feature_list = []
    for _, row in data.iterrows():
        feats = extract_features(row)
        feats["label"] = row["label"]
        feature_list.append(feats)
    return pd.DataFrame(feature_list)
