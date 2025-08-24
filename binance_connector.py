
import requests
import time
import hmac
import hashlib

BASE_URL = "https://api.binance.com"

def sign_request(params, secret_key):
    query_string = "&".join([f"{key}={value}" for key, value in params.items()])
    signature = hmac.new(secret_key.encode(), query_string.encode(), hashlib.sha256).hexdigest()
    return f"{query_string}&signature={signature}"

def execute_binance_trade(user, signal_data):
    api_key = user["api_key"]
    api_secret = user["api_secret"]
    symbol = signal_data["symbol"]
    side = signal_data["signal"]
    amount = 50  # Fixed size for testing; can be replaced with risk logic

    timestamp = int(time.time() * 1000)
    params = {
        "symbol": symbol,
        "side": side.upper(),
        "type": "MARKET",
        "quantity": amount,
        "timestamp": timestamp
    }

    try:
        signed_query = sign_request(params, api_secret)
        headers = {"X-MBX-APIKEY": api_key}
        url = f"{BASE_URL}/api/v3/order?{signed_query}"
        response = requests.post(url, headers=headers)

        if response.status_code == 200:
            return {
                "status": "executed",
                "broker": "binance",
                "symbol": symbol,
                "side": side,
                "details": response.json()
            }
        else:
            return {
                "status": "error",
                "broker": "binance",
                "error": response.text
            }
    except Exception as e:
        return {"status": "error", "broker": "binance", "exception": str(e)}
