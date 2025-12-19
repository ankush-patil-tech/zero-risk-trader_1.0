from newsapi import NewsApiClient
from django.conf import settings
from django.utils.dateparse import parse_datetime
from auth_app.models import StockNews

newsapi = NewsApiClient(api_key=settings.NEWS_API_KEY)

STOCKS = {
    "TCS": "Tata Consultancy Services stock",
    "RELIANCE": "Reliance Industries stock",
    "HDFCBANK": "HDFC Bank stock",
    "BHARTIARTL": "Bharti Airtel stock",
    "ICICIBANK": "ICICI Bank stock"
}


def store_news_for_user(user):
    """
    Fetch news and store RAW news in StockNews table
    """

    for stock, query in STOCKS.items():
        response = newsapi.get_everything(
            q=query,
            language="en",
            sort_by="publishedAt",
            page_size=20
        )

        for article in response.get("articles", []):
            StockNews.objects.get_or_create(
                user=user,
                stock_name=stock,
                headline=article.get("title"),
                source=article.get("source", {}).get("name"),
                published_at=parse_datetime(article.get("publishedAt")),
                content=article.get("content") or ""
            )

    print("✅ Raw news stored successfully")

