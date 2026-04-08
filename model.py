import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import pickle, os

MODEL_PATH  = "trained_model.pkl"
SCALER_PATH = "scaler.pkl"

def generate_training_data():
    np.random.seed(42)
    n          = 500
    mid1       = np.random.uniform(5, 30, n)
    mid2       = np.random.uniform(5, 30, n)
    practical  = np.random.uniform(10, 50, n)
    attendance = np.random.uniform(30, 100, n)
    total = (0.35*mid1 + 0.35*mid2 + 0.25*practical +
             0.05*attendance + np.random.normal(0, 2, n))
    total = np.clip(total, 0, 110)
    return np.column_stack([mid1, mid2, practical, attendance]), total

def train_model():
    X, y    = generate_training_data()
    scaler  = StandardScaler()
    X_sc    = scaler.fit_transform(X)
    model   = LinearRegression()
    model.fit(X_sc, y)
    pickle.dump(model,  open(MODEL_PATH,  'wb'))
    pickle.dump(scaler, open(SCALER_PATH, 'wb'))
    print("✅ Model trained and saved.")
    return model, scaler

def load_model():
    if not os.path.exists(MODEL_PATH):
        return train_model()
    return (pickle.load(open(MODEL_PATH,  'rb')),
            pickle.load(open(SCALER_PATH, 'rb')))

def predict_score(mid1, mid2, practical, attendance):
    model, scaler = load_model()
    feat = np.array([[mid1, mid2, practical, attendance]])
    pred = model.predict(scaler.transform(feat))[0]
    return round(float(np.clip(pred, 0, 110)), 2)

def calculate_grade(total, max_marks=110):
    pct = (total / max_marks) * 100
    if pct >= 90: return 'O'
    if pct >= 75: return 'A+'
    if pct >= 60: return 'A'
    if pct >= 50: return 'B'
    if pct >= 40: return 'C'
    return 'F'