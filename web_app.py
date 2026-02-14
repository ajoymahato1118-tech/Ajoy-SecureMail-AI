from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)

# Increase the data limit so you don't get the "Entity Too Large" error
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 

# Load your high-intelligence TF-IDF brain
model = pickle.load(open('model.pkl', 'rb'))
tfidf = pickle.load(open('vectorizer.pkl', 'rb'))

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Ajoy SecureMail AI | Professional Security Resource</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        <style>
            :root { --primary-blue: #2563eb; --deep-navy: #0f172a; --bg-gray: #f8fafc; }
            body { background-color: var(--bg-gray); font-family: 'Inter', sans-serif; }
            
            /* High-End Header with Logo */
            .navbar { background: white; border-bottom: 2px solid #e2e8f0; padding: 1.2rem 0; }
            .logo-icon { color: var(--primary-blue); font-size: 2.2rem; margin-right: 15px; }
            .brand-name { font-weight: 900; font-size: 1.8rem; color: var(--deep-navy); letter-spacing: -1.5px; }

            /* Professional Scanner Window */
            .main-content { max-width: 900px; margin: 60px auto; }
            .pro-card { background: white; border-radius: 30px; padding: 50px; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1); border: 1px solid #e2e8f0; }
            textarea { border-radius: 15px !important; border: 2px solid #f1f5f9 !important; padding: 20px !important; font-size: 1.1rem !important; }
            .btn-action { background: var(--primary-blue); border: none; border-radius: 15px; padding: 18px; font-weight: 800; font-size: 1.1rem; transition: 0.3s; }
            .btn-action:hover { transform: translateY(-3px); box-shadow: 0 10px 20px rgba(37, 99, 235, 0.3); }

            /* Install Section */
            .install-box { background: #eef2ff; border-radius: 20px; padding: 30px; margin-top: 40px; border-left: 6px solid var(--primary-blue); }
            code { background: var(--deep-navy); color: #38bdf8; padding: 15px; display: block; border-radius: 12px; margin-top: 15px; font-size: 0.9rem; }
        </style>
    </head>
    <body>
        <nav class="navbar shadow-sm">
            <div class="container d-flex justify-content-between align-items-center">
                <div class="d-flex align-items-center">
                    <i class="fas fa-shield-halved logo-icon"></i>
                    <span class="brand-name">AJOY <span style="color: var(--primary-blue);">SECUREMAIL AI</span></span>
                </div>
                <div class="badge bg-primary rounded-pill px-3 py-2">GLOBAL RESOURCE v3.0</div>
            </div>
        </nav>

        <div class="container main-content">
            <div class="pro-card">
                <h3 class="fw-bold mb-4 text-center">Neural Threat Analysis Hub</h3>
                <form action="/predict" method="post">
                    <div class="mb-4">
                        <label class="form-label text-muted small fw-bold"><i class="fas fa-code me-2"></i>SOURCE MESSAGE BODY</label>
                        <textarea name="email_text" class="form-control" rows="10" placeholder="Paste full message content for professional-grade AI auditing..."></textarea>
                    </div>
                    <button type="submit" class="btn btn-primary w-100 btn-action">EXECUTE INTELLIGENT SCAN</button>
                </form>

                <div class="install-box">
                    <h5 class="fw-bold"><i class="fas fa-download me-2"></i>Developer Integration (Installable)</h5>
                    <p class="text-muted small">Searchable API Resource: Other developers can "install" your AI brain by calling this endpoint in their Python, Java, or Node.js systems.</p>
                    <label class="small fw-bold text-primary">ENDPOINT URL:</label>
                    <code>POST http://127.0.0.1:5000/api/scan</code>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/predict', methods=['POST'])
def predict():
    text = request.form['email_text']
    data = tfidf.transform([text]).toarray()
    
    # Advanced: Calculate Confidence Percentage
    prediction = model.predict(data)
    prob = model.predict_proba(data)[0]
    confidence = round(np.max(prob) * 100, 2)
    
    is_spam = prediction[0] == 'spam'
    result_title = "CRITICAL THREAT" if is_spam else "SECURITY VERIFIED"
    res_color = "#dc2626" if is_spam else "#16a34a"

    return f"""
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <body style="background: #f1f5f9; height: 100vh; display: flex; align-items: center; justify-content: center; font-family: sans-serif;">
        <div class="card p-5 text-center shadow-lg border-0" style="width: 550px; border-radius: 40px; background: white;">
            <div style="font-size: 5rem; margin-bottom: 20px;">{'⚠️' if is_spam else '🛡️'}</div>
            <h1 style="font-weight: 900; color: {res_color};">{result_title}</h1>
            <div class="progress my-4" style="height: 35px; border-radius: 20px;">
                <div class="progress-bar" style="width: {confidence}%; background-color: {res_color}; font-weight: bold; line-height: 35px;">AI CONFIDENCE: {confidence}%</div>
            </div>
            <p class="text-secondary mb-4">Ajoy's AI Engine has analyzed the linguistic signature and is {confidence}% sure this message is { "malicious" if is_spam else "authentic" }.</p>
            <a href="/" class="btn btn-dark btn-lg w-100 py-3 rounded-4 fw-bold">Return to Dashboard</a>
        </div>
    </body>
    """

# API for other systems to search and "install" your logic
@app.route('/api/scan', methods=['POST'])
def api_scan():
    input_data = request.json
    text = input_data.get('text', '')
    data = tfidf.transform([text]).toarray()
    prediction = model.predict(data)
    return jsonify({
        "status": "success",
        "result": prediction[0],
        "provider": "Ajoy-SecureMail-AI-Resource"
    })

if __name__ == "__main__":
    app.run(debug=True)