import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Path to your dataset
DATASET_PATH = r"C:\Users\tnraj\Downloads\CloudFarm1\CloudFarm\cloudfarm_project\cloudfarm_app\filled_crop_fertilizer_dataset - filled_crop_fertilizer_dataset.csv.csv"

def load_and_train_models():
    """Load data, train ensemble models, and return them along with encoders."""
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

    # Split data
    X_train, _, y_crop_train, _ = train_test_split(X, y_crop, test_size=0.2, random_state=42)
    _, _, y_fertilizer_train, _ = train_test_split(X, y_fertilizer, test_size=0.2, random_state=42)

    # Define individual models
    rf_model = RandomForestClassifier(random_state=42)
    gb_model = GradientBoostingClassifier(random_state=42)
    lr_model = LogisticRegression(max_iter=500, random_state=42)

    # Create VotingClassifier for crop
    crop_model = VotingClassifier(
        estimators=[
            ("RandomForest", rf_model),
            ("GradientBoosting", gb_model),
            ("LogisticRegression", lr_model),
        ],
        voting="soft"
    )
    crop_model.fit(X_train, y_crop_train)

    # Create VotingClassifier for fertilizer
    fertilizer_model = VotingClassifier(
        estimators=[
            ("RandomForest", rf_model),
            ("GradientBoosting", gb_model),
            ("LogisticRegression", lr_model),
        ],
        voting="soft"
    )
    fertilizer_model.fit(X_train, y_fertilizer_train)

    return crop_model, fertilizer_model, label_encoder_crop, label_encoder_fertilizer

# Load models and encoders
CROP_MODEL, FERTILIZER_MODEL, CROP_ENCODER, FERTILIZER_ENCODER = load_and_train_models()

def predict_crop_and_fertilizer(n, p, k, rainfall, ph):
    """Predict the crop and fertilizer based on input parameters."""
    input_features = [[n, p, k, rainfall, ph]]

    # Predict with VotingClassifier
    crop_predictions = CROP_MODEL.predict_proba(input_features)
    fertilizer_predictions = FERTILIZER_MODEL.predict_proba(input_features)

    # Determine strongest algorithm for crop prediction
    crop_contributions = {name: model.predict_proba(input_features)[0][CROP_MODEL.classes_ == max(crop_predictions[0])] 
                          for name, model in CROP_MODEL.named_estimators_.items()}
    strongest_crop_model = max(crop_contributions, key=crop_contributions.get)

    # Determine strongest algorithm for fertilizer prediction
    fertilizer_contributions = {name: model.predict_proba(input_features)[0][FERTILIZER_MODEL.classes_ == max(fertilizer_predictions[0])] 
                                 for name, model in FERTILIZER_MODEL.named_estimators_.items()}
    strongest_fertilizer_model = max(fertilizer_contributions, key=fertilizer_contributions.get)

    predicted_crop = CROP_ENCODER.inverse_transform([CROP_MODEL.predict(input_features)[0]])
    predicted_fertilizer = FERTILIZER_ENCODER.inverse_transform([FERTILIZER_MODEL.predict(input_features)[0]])

    return {
        "predicted_crop": predicted_crop[0],
        "strongest_crop_model": strongest_crop_model,
        "predicted_fertilizer": predicted_fertilizer[0],
        "strongest_fertilizer_model": strongest_fertilizer_model,
    }