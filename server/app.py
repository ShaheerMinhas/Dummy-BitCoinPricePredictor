from flask import Flask, request, jsonify
import numpy as np
import joblib

app = Flask(__name__)

# Load model and scalers
model = joblib.load("best_model.pkl")
input_scaler = joblib.load("input_scaler.pkl")
target_scaler = joblib.load("target_scaler.pkl")

@app.after_request
def add_cors_headers(response):
    response.headers.add("Access-Control-Allow-Origin", "https://bitcoin-predict-dummy.netlify.app")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
    return response

@app.route('/predict', methods=['POST', 'OPTIONS'])
def predict():
    if request.method == 'OPTIONS':
        # Preflight request
        return '', 204

    try:
        data = request.get_json()
        high = float(data['high'])
        low = float(data['low'])

        input_data = np.array([[high, low]])
        input_scaled = input_scaler.transform(input_data)
        pred_scaled = model.predict(input_scaled)
        pred_actual = target_scaler.inverse_transform(pred_scaled.reshape(-1, 1))

        return jsonify({'predicted_close': round(float(pred_actual[0][0]), 2)})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
