import os
import pickle
from flask import Flask, render_template, request, jsonify
import numpy as np

app = Flask(__name__)

# -----------------------------
# Load Model & Vectorizer
# -----------------------------
try:
    with open("model.pkl", "rb") as model_file:
        model = pickle.load(model_file)

    with open("vectorizer.pkl", "rb") as vectorizer_file:
        vectorizer = pickle.load(vectorizer_file)

    print("Model and vectorizer loaded successfully.")

except Exception as e:
    print("Error loading model:", e)
    model = None
    vectorizer = None


# -----------------------------
# Helper Function
# -----------------------------
def predict_email(text):
    if not model or not vectorizer:
        return None

    transformed_text = vectorizer.transform([text])
    prediction = model.predict(transformed_text)[0]

    # Probability (confidence)
    if hasattr(model, "predict_proba"):
        probability = model.predict_proba(transformed_text)[0]
        confidence = np.max(probability) * 100
    else:
        confidence = 95.0  # fallback

    result = "Spam" if prediction == 1 else "Not Spam"

    # Risk level
    if confidence >= 90:
        risk = "High"
    elif confidence >= 70:
        risk = "Medium"
    else:
        risk = "Low"

    return {
        "result": result,
        "confidence": round(confidence, 2),
        "risk": risk
    }


# -----------------------------
# Routes
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    email_text = request.form.get("email")

    if not email_text or email_text.strip() == "":
        return render_template("index.html", error="Please enter email text.")

    prediction = predict_email(email_text)

    if not prediction:
        return render_template("index.html", error="Model not loaded properly.")

    return render_template(
        "index.html",
        result=prediction["result"],
        confidence=prediction["confidence"],
        risk=prediction["risk"]
    )


# -----------------------------
# API Endpoint (Optional but Professional)
# -----------------------------
@app.route("/api/predict", methods=["POST"])
def api_predict():
    data = request.get_json()

    if not data or "email" not in data:
        return jsonify({"error": "No email provided"}), 400

    prediction = predict_email(data["email"])

    if not prediction:
        return jsonify({"error": "Model not loaded"}), 500

    return jsonify(prediction)


# -----------------------------
# Run App (Production Ready)
# -----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
