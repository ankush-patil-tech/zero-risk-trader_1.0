def generate_final_signal(sentiments):
    score = 0

    for s in sentiments:
        if s["sentiment"] == "positive":
            score += s["confidence"]
        elif s["sentiment"] == "negative":
            score -= s["confidence"]

    if score > 1.5:
        return "BUY"
    elif score < -1.5:
        return "SELL"
    else:
        return "HOLD"
