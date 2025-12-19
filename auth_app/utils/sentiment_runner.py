from auth_app.services.news_fetcher import store_news_for_user
from auth_app.services.news_processing import process_news_for_user
from auth_app.models import UserSentimentStatus


def run_sentiment_background(user):
    try:
        status, _ = UserSentimentStatus.objects.get_or_create(user=user)
        status.status = "RUNNING"
        status.save()

        store_news_for_user(user)
        process_news_for_user(user)

        status.status = "DONE"
        status.save()

    except Exception as e:
        status.status = "FAILED"
        status.save()
        print("Sentiment error:", e)
