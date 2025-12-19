from .azure_openai_client import client
import json
import os


def analyze_news_sentiment(stock_name: str, news: dict) -> dict:
    """
    Returns sentiment analysis as JSON:
    { sentiment, confidence, reason }
    """

    prompt = f"""
Analyze sentiment of stock news.

Stock: {stock_name}

Headline: {news.get("headline")}
Source: {news.get("source")}
Published At: {news.get("published_at")}

News Content:
"{news.get("content", "")}"

Return ONLY valid JSON:
{{
  "sentiment": "positive | neutral | negative",
  "confidence": 0.0,
  "reason": "short explanation"
}}
"""

    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),  # ✅ CORRECT
        messages=[
            {"role": "system", "content": "You are a financial sentiment analysis engine."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=200,
    )

    return json.loads(response.choices[0].message.content)


def summarize_stock_news(stock_name: str, news_list: list) -> str:
    """
    Summarize all latest news for a stock and give a low-risk action.
    """

    if not news_list:
        return "No recent news available to generate a summary."

    news_text = "\n".join(
        f"- {n.get('headline','')} ({n.get('sentiment','')}, {n.get('confidence','')})"
        for n in news_list
    )

    prompt = f"""
You are a conservative, risk-aware financial assistant.

Stock: {stock_name}

Latest News:
{news_text}

Your tasks:
1. Summarize overall sentiment in 2–3 lines
2. Mention key positives and risks
3. Suggest a LOW-RISK action:
   - BUY (only if risk is low)
   - HOLD (if mixed/uncertain)
   - AVOID (if negative risk exists)

Rules:
- No hype
- Calm and factual
- Capital protection first
"""

    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),  # ✅ FIXED HERE
        messages=[
            {
                "role": "system",
                "content": "You are a cautious financial assistant focused on capital protection."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_tokens=250,
    )

    return response.choices[0].message.content.strip()


def explain_news_with_price(
    stock_name: str,
    news_summary: str,
    news_sentiment: str,
    news_confidence: float,
    price_data: dict,
    zero_risk: dict
) -> str:
    """
    AI explanation combining NEWS + PRICE + RISK
    """

    prompt = f"""
You are an AI assistant for a conservative trading platform called ZeroRiskTrader.

Stock: {stock_name}

NEWS:
- Sentiment: {news_sentiment}
- Confidence: {news_confidence}
- Summary: {news_summary}

PRICE DATA:
- Trend: {price_data['trend']}
- Latest Close: {price_data['close']}
- 20 DMA: {price_data['dma_20']}
- 50 DMA: {price_data['dma_50']}
- Volatility: {price_data['volatility']}%

ZERORISK SCORE:
- Score: {zero_risk['score']} / 100
- Risk Level: {zero_risk['label']}

TASK:
1. Explain if price CONFIRMS or CONTRADICTS the news
2. Highlight key risks from trend or volatility
3. Justify the ZeroRisk recommendation

RULES:
- No hype
- No prediction
- Focus on capital protection
- Beginner friendly
"""

    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        messages=[
            {"role": "system", "content": "You are a cautious financial analyst."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
        max_tokens=350,
    )

    return response.choices[0].message.content.strip()


def summarize_ml_findings(stock, best_model, performance, news=None):
    prompt = f"""
    You are an AI assistant for a LOW-RISK trading platform.
    Your audience is a beginner retail investor.

    Stock: {stock}

    ML Findings (with values):
    - Best Model: {best_model['model_name']}
    - Success Rate: {best_model['success_rate']}%
    - Directional Accuracy: {best_model['directional_success_rate']}%
    - Average Error: {best_model['average_error']}

    Other Models Performance (success rates):
    {performance}

    News Sentiment (with values):
    - Signal: {news.get('signal') if news else 'Not Available'}
    - Sentiment Confidence: {news.get('confidence') if news else 'Not Available'}
    - News Summary: {news.get('summary') if news else 'No recent news available'}

    Your tasks (STRICT FORMAT):

    ### 1. ML Insight
    Explain what the ML results indicate in ONE short sentence, clearly mentioning at least ONE numeric value.

    ### 2. News Insight
    Explain what the recent news sentiment indicates in ONE short sentence, mentioning the signal and confidence value if available.

    ### 3. Reliability
    Explain overall reliability in ONE short sentence based on ML accuracy and news strength.
    Then output ONE word on next line:
    Reliable / Moderate / Unreliable

    ### 4. Risk Level
    Explain risk in ONE short sentence considering ML error and news alignment.
    Then output ONE word on next line:
    LOW / MEDIUM / HIGH

    ### 5. Suggested Action
    Output EXACTLY in this format:
    Action: BUY | HOLD | AVOID
    Reason: ONE short sentence using ML and news values

    ### 6. Model Agreement
    Explain in ONE sentence whether most ML models show similar performance values.
    Then output ONE word:
    AGREE / MIXED / CONFLICT

    ### 7. Prediction Stability
    Explain in ONE sentence whether predictions appear stable based on accuracy and error values.
    Then output ONE word:
    STABLE / UNSTABLE

    ### 8. Confidence Level
    Explain confidence in ONE sentence using ML success rate and news confidence.
    Then output ONE word:
    HIGH / MEDIUM / LOW

    ### 9. Time Horizon
    In ONE sentence, state suitability for:
    SHORT-TERM / MID-TERM / NOT SUITABLE

    Rules (VERY IMPORTANT):
    - ONE sentence per explanation only
    - NO paragraphs
    - NO hype or promotional language
    - Beginner friendly wording
    - Capital protection first
    - Avoid technical jargon
    - Prefer numbers over adjectives
    """

    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        messages=[
            {"role": "system", "content": "You explain ML predictions cautiously."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=300,
    )

    return response.choices[0].message.content.strip()