from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import joblib

app = Flask(__name__)

# Enable CORS for specific origins
# Apply CORS to all routes and methods with explicit origins
CORS(app, resources={r"/*": {"origins": [
    "http://localhost:3000",
    "https://bitcoin-predict-dummy.netlify.app"
]}}, supports_credentials=True)
# Load model and scalers
model = joblib.load("best_model.pkl")
input_scaler = joblib.load("input_scaler.pkl")
target_scaler = joblib.load("target_scaler.pkl")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get JSON data
        data = request.get_json()
        high = float(data['high'])
        low = float(data['low'])

        # Prepare and scale input
        input_data = np.array([[high, low]])
        input_scaled = input_scaler.transform(input_data)

        # Predict and inverse transform
        pred_scaled = model.predict(input_scaled)
        pred_actual = target_scaler.inverse_transform(pred_scaled.reshape(-1, 1))

        return jsonify({
            'predicted_close': round(float(pred_actual[0][0]), 2)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
