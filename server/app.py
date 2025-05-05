from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np

app = Flask(__name__)
CORS(app)

# Load model and scalers
model = joblib.load("model.pkl")
x_scaler = joblib.load("X_scaler.pkl")
y_scaler = joblib.load("y_scaler.pkl")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        # Expecting keys: 'high' and 'low'
        high = float(data['high'])
        low = float(data['low'])

        # Construct input as [High, Low]
        input_features = np.array([[high, low]])

        # Scale and predict
        scaled_input = x_scaler.transform(input_features)
        scaled_prediction = model.predict(scaled_input)

        # Inverse transform the predicted value
        prediction = y_scaler.inverse_transform(scaled_prediction.reshape(-1, 1)).flatten()[0]

        return jsonify({'predicted_close': round(prediction, 2)})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
