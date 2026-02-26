import pickle
import os
from sklearn.ensemble import RandomForestClassifier

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")


def train_model():
 
    X = [
        [0, 0, 5, 0, 200],
        [1, 1, 120, 3, 200],
        [1, 2, 200, 4, 200],
        [0, 0, 10, 0, 200]
    ]

    y = [0, 1, 1, 0] 

    model = RandomForestClassifier()
    model.fit(X, y)

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)

    return model


def predict(features):
   
    if not os.path.exists(MODEL_PATH) or os.path.getsize(MODEL_PATH) == 0:
        model = train_model()
    else:
        try:
            with open(MODEL_PATH, "rb") as f:
                model = pickle.load(f)
        except:
            model = train_model()

    prediction = model.predict([features])[0]
    probability = model.predict_proba([features])[0][1]

    return prediction, probability