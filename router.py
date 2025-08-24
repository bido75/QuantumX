
import json
from binance_connector import execute_binance_trade
from ibkr_connector import execute_ibkr_trade
from metatrader_connector import execute_metatrader_trade

# Load user configuration file
def load_user_config():
    with open("quantumx_user_config.json", "r") as file:
        return json.load(file)["users"]

# Find user by ID
def find_user(user_id):
    users = load_user_config()
    for user in users:
        if user["user_id"] == user_id:
            return user
    return None

# Route the signal to the correct broker executor
def route_signal(signal_data):
    user_id = signal_data.get("user_id")
    user_profile = find_user(user_id)

    if not user_profile:
        return {"status": "error", "message": "User not found"}

    broker = user_profile.get("broker")

    if broker == "binance":
        return execute_binance_trade(user_profile, signal_data)
    elif broker == "ibkr":
        return execute_ibkr_trade(user_profile, signal_data)
    elif broker == "metatrader":
        return execute_metatrader_trade(user_profile, signal_data)
    else:
        return {"status": "error", "message": f"Unsupported broker: {broker}"}
