from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/health')
def health():
    return jsonify({"status": "ok"})

@app.route('/')
def index():
    return jsonify({"message": "Catacomb API - Innovation Capital Allocation System"})

if __name__ == '__main__':
    app.run(port=5000)
