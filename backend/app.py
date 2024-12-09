from flask import Flask, request, jsonify
from utils.ai_predictor import predict_oral_health

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    """Endpoint for oral health prediction"""
    # Image processing logic here
    return jsonify({"prediction": "result"})

if __name__ == '__main__':
    app.run(debug=True)
