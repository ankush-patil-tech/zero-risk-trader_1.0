from .azure_openai_client import get_azure_openai_client
import os
import json
import re


# =====================================================
# 🔒 SAFE JSON PARSER (ONLY FOR SENTIMENT CLASSIFIER)
# =====================================================

def safe_json_extract(text):
    try:
        match = re.search(r"\{.*\}", text, re.S)
        if not match:
            raise ValueError("No JSON found")

        return json.loads(match.group())

    except Exception:
        return {
            "sentiment": "neutral",
            "confidence": 0.5,
            "reason": "AI output parsing fallback"
        }


# =====================================================
# ✅ NEWS SENTIMENT ANALYSIS (RETURNS JSON)
# =====================================================

def analyze_news_sentiment(stock_name: str, news: dict) -> dict:
    """
    Returns:
    {
      sentiment: positive | neutral | negative,
      confidence: float,
      reason: string
    }
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

    client = get_azure_openai_client()

    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        messages=[
            {"role": "system", "content": "You are a financial sentiment analysis engine."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=200,
    )

    raw_output = response.choices[0].message.content

    # ✅ JSON ONLY HERE
    return safe_json_extract(raw_output)


# =====================================================
# ✅ AI NEWS SUMMARY (RETURNS PURE TEXT)
# =====================================================

def summarize_stock_news(stock_name: str, news_list: list) -> str:
    """
    Returns readable formatted text (NOT JSON)
    """

    if not news_list:
        return "No recent news available to generate a summary."

    news_text = "\n".join(
        f"- {n.get('headline', '')} ({n.get('sentiment', '')}, {n.get('confidence', '')})"
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
   - HOLD (if mixed)
   - AVOID (if risk exists)

Rules:
- No hype
- Calm and factual
- Capital protection first
"""

    client = get_azure_openai_client()

    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        messages=[
            {"role": "system", "content": "You are a cautious financial assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=300,
    )

    # ✅ RETURN STRING ONLY
    return response.choices[0].message.content.strip()


# =====================================================
# ✅ NEWS + PRICE + RISK EXPLANATION (TEXT)
# =====================================================

def explain_news_with_price(
    stock_name: str,
    news_summary: str,
    news_sentiment: str,
    news_confidence: float,
    price_data: dict,
    zero_risk: dict
) -> str:

    prompt = f"""
You are an AI assistant for ZeroRiskTrader.

Stock: {stock_name}

NEWS:
- Sentiment: {news_sentiment}
- Confidence: {news_confidence}
- Summary: {news_summary}

PRICE DATA:
- Trend: {price_data['trend']}
- Close: {price_data['close']}
- 20 DMA: {price_data['dma_20']}
- 50 DMA: {price_data['dma_50']}
- Volatility: {price_data['volatility']}%

ZERORISK SCORE:
- Score: {zero_risk['score']}
- Risk Level: {zero_risk['label']}

Explain carefully:
1. Whether price confirms news
2. Key risks
3. Why ZeroRisk recommendation fits

Rules:
- No prediction
- No hype
- Capital protection first
"""

    client = get_azure_openai_client()

    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        messages=[
            {"role": "system", "content": "You are a cautious financial analyst."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
        max_tokens=350,
    )

    # ✅ TEXT
    return response.choices[0].message.content.strip()


# =====================================================
# ✅ ML FINDINGS SUMMARY (PRODUCTION SAFE)
# =====================================================
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

    try:
        client = get_azure_openai_client()

        response = client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            messages=[
                {"role": "system", "content": "You explain ML predictions cautiously."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=350,
        )

        text = response.choices[0].message.content

        # 🔒 SAFETY CHECK
        if not text or not text.strip():
            raise ValueError("Empty AI response")

        return text.strip()

    except Exception as e:
        print("🔥 ML AI SUMMARY ERROR:", e)

        # ✅ SAFE FALLBACK (UI WILL NEVER BREAK)
        return f"""
### AI Summary Unavailable

### 1. ML Insight
Model results could not be evaluated at this moment due to system limitations.

### 2. News Insight
News sentiment analysis could not be combined reliably.

### 3. Reliability
Data quality is currently insufficient.
Unreliable

### 4. Risk Level
Risk cannot be assessed confidently.
HIGH

### 5. Suggested Action
Action: HOLD
Reason: Insufficient validated AI output for capital-safe decision.

### 6. Model Agreement
Model comparison could not be completed.
MIXED

### 7. Prediction Stability
Prediction stability cannot be confirmed.
UNSTABLE

### 8. Confidence Level
Overall confidence is low due to missing AI validation.
LOW

### 9. Time Horizon
NOT SUITABLE
"""
