# train_model.py
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

from data_preparation import load_dataset
from feature_engineering import create_feature_set

def main():
    # โหลด dataset จริง
    raw_data = load_dataset()
    print("Raw data shape:", raw_data.shape)

    # สร้าง features
    feature_data = create_feature_set(raw_data)
    print("Feature data shape:", feature_data.shape)

    # Train/Test split
    X = feature_data.drop("label", axis=1)
    y = feature_data["label"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Train RandomForest
    clf = RandomForestClassifier(n_estimators=200, random_state=42)
    clf.fit(X_train, y_train)

    # Evaluate
    y_pred = clf.predict(X_test)
    print(classification_report(y_test, y_pred))

    # Save model
    joblib.dump(clf, "asl_model.pkl")
    print("Model saved as asl_model.pkl")

if __name__ == "__main__":
    main()
