import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Path to your dataset
DATASET_PATH = r"C:\Users\tnraj\Downloads\CloudFarm1\CloudFarm\cloudfarm_project\cloudfarm_app\filled_crop_fertilizer_dataset - filled_crop_fertilizer_dataset.csv"


def load_and_train_models():
    """Load data, train models, and return them along with encoders."""
    data = pd.read_csv(DATASET_PATH)

    # Preprocess data
    data = data.drop(columns=["humidity"])
    label_encoder_crop = LabelEncoder()
    label_encoder_fertilizer = LabelEncoder()
    data["label"] = label_encoder_crop.fit_transform(data["label"])
    data["Fertilizer"] = label_encoder_fertilizer.fit_transform(data["Fertilizer"])

    # Features and targets
    X = data[["N", "P", "K", "rainfall", "ph"]]
    y_crop = data["label"]
    y_fertilizer = data["Fertilizer"]

    # Split and train models
    X_train, _, y_crop_train, _ = train_test_split(X, y_crop, test_size=0.2, random_state=42)
    _, _, y_fertilizer_train, _ = train_test_split(X, y_fertilizer, test_size=0.2, random_state=42)

    crop_model = RandomForestClassifier(random_state=42)
    fertilizer_model = RandomForestClassifier(random_state=42)
    crop_model.fit(X_train, y_crop_train)
    fertilizer_model.fit(X_train, y_fertilizer_train)

    return crop_model, fertilizer_model, label_encoder_crop, label_encoder_fertilizer

# Load models and encoders
CROP_MODEL, FERTILIZER_MODEL, CROP_ENCODER, FERTILIZER_ENCODER = load_and_train_models()

def predict_crop_and_fertilizer(n, p, k, rainfall, ph):
    """Predict the crop and fertilizer based on input parameters."""
    input_features = [[n, p, k, rainfall, ph]]
    predicted_crop = CROP_ENCODER.inverse_transform(CROP_MODEL.predict(input_features))
    predicted_fertilizer = FERTILIZER_ENCODER.inverse_transform(FERTILIZER_MODEL.predict(input_features))
    return {
        "predicted_crop": predicted_crop[0],
        "predicted_fertilizer": predicted_fertilizer[0],
    }
