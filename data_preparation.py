# data_preparation.py
import pandas as pd

def load_dataset(file_path=r"C:\Homework\dobot_hand_control\asl_data.csv"):
    """
    Load XYZ dataset.
    Format: Each row = [x0,y0,z0, x1,y1,z1, ..., label]
    """
    data = pd.read_csv(file_path)
    return data
