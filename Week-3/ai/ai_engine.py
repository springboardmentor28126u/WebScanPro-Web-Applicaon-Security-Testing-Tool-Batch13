import pickle
import os
from sklearn.linear_model import LogisticRegression

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")


def train_model():
    # Updated dataset (4 features now)
    X = [
        [10, 0, 200, 0.01],
        [200, 2, 500, 0.05],
        [150, 1, 200, 0.04],
        [5, 0, 200, 0.01]
    ]

    y = [0, 1, 1, 0]  # 0 = safe, 1 = vulnerable

    model = LogisticRegression()
    model.fit(X, y)

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)

    return model


def load_model():
    # If file missing OR empty → retrain
    if not os.path.exists(MODEL_PATH) or os.path.getsize(MODEL_PATH) == 0:
        return train_model()

    try:
        with open(MODEL_PATH, "rb") as f:
            model = pickle.load(f)

        # Ensure correct feature size (4)
        if model.coef_.shape[1] != 4:
            return train_model()

        return model

    except:
        return train_model()


def predict(features):
    model = load_model()

    prediction = model.predict([features])[0]
    probability = model.predict_proba([features])[0][1]

    return prediction, probability