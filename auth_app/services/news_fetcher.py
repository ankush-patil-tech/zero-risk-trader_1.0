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
    Fetch news and store RAW news in StockNews table (SAFE)
    """

    for stock, query in STOCKS.items():
        response = newsapi.get_everything(
            q=query,
            language="en",
            sort_by="publishedAt",
            page_size=20
        )

        for article in response.get("articles", []):

            headline = article.get("title") or ""
            content = article.get("content") or ""
            source = article.get("source", {}).get("name") or ""

            published_at_raw = article.get("publishedAt")
            published_at = (
                parse_datetime(published_at_raw)
                if published_at_raw else None
            )

            # ❗ skip useless articles
            if not headline.strip():
                continue

            StockNews.objects.get_or_create(
                user=user,
                stock_name=stock,
                headline=headline.strip(),
                source=source.strip(),
                published_at=published_at,
                content=content.strip()
            )

    print("✅ Raw news stored successfully")
