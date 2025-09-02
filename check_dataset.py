import pandas as pd

def main():
    # โหลด dataset (แก้ path ตรงนี้ถ้าไฟล์อยู่ที่อื่น)
    file_path = r"C:\Homework\dobot_hand_control\asl_data.csv"

    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"❌ ไม่พบไฟล์: {file_path}")
        return

    print("✅ โหลด dataset สำเร็จ\n")

    # ดูชื่อคอลัมน์ทั้งหมด
    print("📌 Columns:")
    print(df.columns.tolist())
    print("\n")

    # ดูขนาด dataset
    print("📊 Shape (rows, cols):", df.shape)
    print("\n")

    # ดูตัวอย่างข้อมูล 5 แถวแรก
    print("🔎 Head (5 rows):")
    print(df.head())
    print("\n")

    # ดูรายละเอียดเบื้องต้น
    print("ℹ️ Info:")
    print(df.info())

if __name__ == "__main__":
    main()
