
# QuantumX Risk Engine
# Calculates dynamic position sizing per user config and signal data

def calculate_position_size(user_profile, signal_data, asset_price, stop_loss_pct):
    risk_pct = user_profile["risk_settings"]["risk_per_trade_pct"]
    max_drawdown = user_profile["risk_settings"]["max_drawdown_pct"]

    # Assume fixed capital or pull from user config
    capital = user_profile.get("capital", 10000)  # Default $10,000
    risk_amount = (risk_pct / 100.0) * capital

    # Calculate amount based on stop loss
    if stop_loss_pct == 0:
        stop_loss_pct = 1  # prevent div-by-zero

    # position size = risk_amount / (price * stop_loss_percent)
    position_size = risk_amount / (asset_price * (stop_loss_pct / 100.0))
    position_size = round(position_size, 4)

    return {
        "capital": capital,
        "risk_pct": risk_pct,
        "risk_amount": round(risk_amount, 2),
        "stop_loss_pct": stop_loss_pct,
        "asset_price": asset_price,
        "position_size": position_size
    }
