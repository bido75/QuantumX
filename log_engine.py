
# QuantumX Log Engine
# Logs all trade actions with status, timestamp, and broker info

import json
from datetime import datetime

LOG_FILE = "quantumx_trades_log.jsonl"  # JSON Lines format

def log_trade(user_id, broker, symbol, side, quantity, status, details=None):
    timestamp = datetime.utcnow().isoformat()

    log_entry = {
        "timestamp": timestamp,
        "user_id": user_id,
        "broker": broker,
        "symbol": symbol,
        "side": side,
        "quantity": quantity,
        "status": status,
        "details": details or {}
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

    return log_entry
