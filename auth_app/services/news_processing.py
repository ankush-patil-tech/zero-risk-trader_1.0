from datetime import datetime
from auth_app.models import StockNews, StockNewsSentiment
from .sentiment_service import analyze_news_sentiment


def calculate_final_signal(news_results):
    positive = sum(1 for n in news_results if n["sentiment"] == "positive")
    negative = sum(1 for n in news_results if n["sentiment"] == "negative")

    if positive >= negative + 2:
        return "BUY"
    if negative >= positive + 2:
        return "SELL"
    return "HOLD"


def calculate_sentiment_score(news_results):
    if not news_results:
        return 0

    score = 0
    for n in news_results:
        if n["sentiment"] == "positive":
            score += n["confidence"]
        elif n["sentiment"] == "negative":
            score -= n["confidence"]

    # Normalize to 0–100 for UI
    return round(max(min(score * 100, 100), 0), 2)


def process_news_for_user(user):
    """
    Analyze stored news for a user and persist sentiment results
    """

    news_qs = StockNews.objects.filter(user=user)

    stock_map = {}

    for news in news_qs:
        result = analyze_news_sentiment(
            stock_name=news.stock_name,
            news={
                "headline": news.headline,
                "source": news.source,
                "published_at": news.published_at.isoformat(),
                "content": news.content,
            }
        )

        stock_map.setdefault(news.stock_name, []).append({
            "headline": news.headline,
            "source": news.source,
            "published_at": news.published_at.strftime("%Y-%m-%d %H:%M"),
            "sentiment": result.get("sentiment"),
            "confidence": result.get("confidence"),
            "reason": result.get("reason"),
        })

    today = datetime.now().date()

    for stock_name, news_list in stock_map.items():
        final_signal = calculate_final_signal(news_list)
        sentiment_score = calculate_sentiment_score(news_list)

        StockNewsSentiment.objects.update_or_create(
            user=user,
            stock_name=stock_name,
            last_refresh_data=today,
            defaults={
                "meta_data": {
                    "final_signal": final_signal,
                    "sentiment_score": sentiment_score,
                    "news": news_list,
                    "last_updated": datetime.now().isoformat()
                }
            }
        )
