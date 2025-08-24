from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "YOUR_API_KEY"
THREE_COMMAS_URL = "https://api.3commas.io/public/api/v2/smart_trades"

@app.route('/webhook/quantumx', methods=['POST'])
def quantumx_webhook():
    data = request.get_json()
    symbol = data.get("symbol", "BTCUSDT")
    signal = data.get("signal", "")
    confidence = data.get("confidence", 0.0)

    if signal not in ["BUY", "SELL"]:
        return jsonify({"status": "ignored", "reason": "No trade signal"})

    payload = {
        "symbol": symbol,
        "side": signal,
        "confidence": confidence,
        "amount_usd": 100
    }

    response = requests.post(
        THREE_COMMAS_URL,
        headers={"Authorization": f"Bearer {API_KEY}"},
        json=payload
    )

    return jsonify({"status": "executed", "signal": signal, "symbol": symbol, "response": response.json()})
