from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)
model = joblib.load("fraud_model.pkl")
scaler = joblib.load("scaler.pkl")
@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    input_data = np.array(data).reshape(1, -1)
    input_scaled = scaler.transform(input_data)
    prediction = model.predict(input_scaled)
    return jsonify({"result": int(prediction[0])})
if __name__ == "__main__":
    app.run(debug=True)