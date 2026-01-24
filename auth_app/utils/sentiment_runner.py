
from django.contrib.auth.models import User
from django.utils import timezone

from auth_app.services.news_fetcher import store_news_for_user
from auth_app.services.news_processing import process_news_for_user
from auth_app.models import UserSentimentStatus


def run_sentiment_background(user_id):
    try:
        user = User.objects.get(id=user_id)

        status, _ = UserSentimentStatus.objects.get_or_create(user=user)
        status.status = "RUNNING"
        status.started_at = timezone.now()
        status.save()

        store_news_for_user(user)
        process_news_for_user(user)

        status.status = "DONE"
        status.finished_at = timezone.now()
        status.save()

    except Exception as e:
        status.status = "FAILED"
        status.error_message = str(e)
        status.save()
        print("🔥 Sentiment error:", e)
