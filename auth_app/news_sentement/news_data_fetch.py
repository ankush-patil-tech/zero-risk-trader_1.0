# from datetime import date
# from newsapi import NewsApiClient
# from django.conf import settings
# from auth_app.models import StockNewsSentiment

# # Initialize NewsAPI
# newsapi = NewsApiClient(api_key=settings.NEWS_API_KEY)

# STOCKS = {
#     "TCS": "Tata Consultancy Services stock",
#     "RELIANCE": "Reliance Industries stock",
#     "HDFCBANK": "HDFC Bank stock",
#     "BHARTIARTL": "Bharti Airtel stock",
#     "ICICIBANK": "ICICI Bank stock"
# }


# def store_news_for_user(user):
#     """
#     Fetch news and store ONLY RAW NEWS in DB
#     """
#     today = date.today()

#     for stock, query in STOCKS.items():
#         print(f"Fetching news for {stock}")

#         response = newsapi.get_everything(
#             q=query,
#             language="en",
#             sort_by="publishedAt",
#             page_size=100
#         )

#         news_list = []

#         for article in response.get("articles", []):
#             news_list.append({
#                 "headline": article.get("title"),
#                 "source": article.get("source", {}).get("name"),
#                 "published_at": article.get("publishedAt")
#             })

#         StockNewsSentiment.objects.update_or_create(
#             user=user,
#             stock_name=stock,
#             last_refresh_data=today,
#             defaults={
#                 "meta_data": {
#                     "news": news_list,
#                     "final_signal": None  # will be filled later
#                 }
#             }
#         )

#     print("✅ News stored successfully")
