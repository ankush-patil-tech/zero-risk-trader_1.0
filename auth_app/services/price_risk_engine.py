from statistics import mean


def calculate_trend(closes: list[float]) -> str:
    """
    Simple trend detection using last N closes
    """
    if len(closes) < 5:
        return "sideways"

    if closes[-1] > closes[-5]:
        return "uptrend"
    elif closes[-1] < closes[-5]:
        return "downtrend"
    return "sideways"


def calculate_volatility(highs, lows, closes) -> float:
    """
    Average daily volatility percentage
    """
    vols = [
        (h - l) / c * 100
        for h, l, c in zip(highs, lows, closes)
        if c > 0
    ]
    return round(mean(vols), 2) if vols else 0.0


def moving_average(values, period: int) -> float:
    if len(values) < period:
        return mean(values)
    return mean(values[-period:])


def compute_zero_risk_score(
    news_sentiment: str,
    news_confidence: float,
    closes: list[float],
    highs: list[float],
    lows: list[float],
):
    """
    Final ZeroRisk score (0–100)
    """

    score = 0

    # ---------------- NEWS SCORE (30)
    if news_sentiment == "positive" and news_confidence >= 0.7:
        score += 30
    elif news_sentiment == "neutral":
        score += 15

    # ---------------- PRICE TREND (30)
    trend = calculate_trend(closes)
    if trend == "uptrend":
        score += 30
    elif trend == "sideways":
        score += 15

    # ---------------- MOVING AVERAGES (20)
    close = closes[-1]
    dma_20 = moving_average(closes, 20)
    dma_50 = moving_average(closes, 50)

    if close > dma_50:
        score += 20
    elif close > dma_20:
        score += 10

    # ---------------- VOLATILITY (20)
    volatility = calculate_volatility(highs, lows, closes)

    if volatility < 1.2:
        score += 20
    elif volatility < 2.5:
        score += 10

    # ---------------- LABEL
    if score >= 80:
        label = "LOW RISK"
    elif score >= 60:
        label = "MODERATE"
    elif score >= 40:
        label = "CAUTION"
    else:
        label = "HIGH RISK"

    return {
        "score": score,
        "label": label,
        "trend": trend,
        "dma_20": round(dma_20, 2),
        "dma_50": round(dma_50, 2),
        "volatility": volatility,
    }
