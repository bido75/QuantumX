
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'QuantumX Engine API Running'

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
