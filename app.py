
from flask import Flask, request, jsonify
import requests
import os
import json
from datetime import datetime

app = Flask(__name__)

API_KEY = os.getenv("API_KEY", "YOUR_API_KEY")
THREE_COMMAS_URL = "https://api.3commas.io/public/api/v2/smart_trades"
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "")

LOG_FILE = "quantumx_signals.json"

@app.route('/')
def home():
    return "QuantumX Engine API Running"

@app.route('/webhook/quantumx', methods=['POST'])
def quantumx_webhook():
    if not request.is_json:
        return jsonify({"status": "error", "message": "Expected application/json"}), 415

    data = request.get_json()
    symbol = data.get("symbol", "BTCUSDT")
    signal = data.get("signal", "").upper()
    confidence = data.get("confidence", 0.0)
    strategy = data.get("strategy", "quantumx")

    if signal not in ["BUY", "SELL"]:
        return jsonify({"status": "ignored", "reason": "No actionable signal"})

    timestamp = datetime.utcnow().isoformat()
    signal_data = {
        "timestamp": timestamp,
        "symbol": symbol,
        "signal": signal,
        "confidence": confidence,
        "strategy": strategy
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(signal_data) + "\n")

    if DISCORD_WEBHOOK_URL:
        try:
            requests.post(DISCORD_WEBHOOK_URL, json={
                "content": f"📈 **QuantumX Signal**\n`{symbol}` → `{signal}` ({confidence*100:.1f}% confidence)\nTime: {timestamp}"
            })
        except Exception as e:
            print(f"[Discord Error] {e}")

    try:
        response = requests.post(
            THREE_COMMAS_URL,
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={
                "symbol": symbol,
                "side": signal,
                "confidence": confidence,
                "amount_usd": 100
            }
        )
        trade_response = response.json()
    except Exception as e:
        return jsonify({"status": "error", "message": f"Execution failed: {e}"}), 500

    return jsonify({
        "status": "executed",
        "signal": signal,
        "symbol": symbol,
        "confidence": confidence,
        "timestamp": timestamp,
        "log_file": LOG_FILE,
        "response": trade_response
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
