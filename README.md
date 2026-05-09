# 📈 ZeroRiskTrader

ZeroRiskTrader is a full-stack AI-powered paper trading platform designed to simulate real-world stock trading without financial risk. The platform enables users to execute virtual trades, analyze stock market trends, track portfolio performance, and leverage machine learning-driven stock predictions with AI-generated market insights.

Built using Django, MySQL, Docker, and Azure cloud infrastructure, the application integrates financial APIs, sentiment analysis, machine learning models, and Azure OpenAI services to deliver an intelligent trading simulation experience.

---

## 🚀 Key Features

- 📊 Real-time paper trading simulation using live market data
- 💼 Portfolio management with profit/loss tracking
- 🤖 Machine Learning-based next-day stock price prediction
- ⚙️ Custom hyperparameter tuning across multiple ML models
- 📈 Comparative evaluation of ML models using performance metrics
- 📰 Financial news sentiment analysis with sentiment scoring
- 🧠 AI-generated summaries of stock trends and market news using Azure OpenAI API
- 🔐 Secure JWT-based authentication and session management
- 🐳 Containerized deployment using Docker & Docker Compose
- ☁️ Cloud deployment on Microsoft Azure
- 🌐 Nginx reverse proxy with HTTPS enabled via Let’s Encrypt
- 🔄 Automated CI/CD workflows using GitHub Actions

---

## 🏗️ System Architecture

```text
                ┌────────────────────┐
                │   Financial APIs   │
                │ Alpha Vantage API  │
                └─────────┬──────────┘
                          │
                          ▼
┌──────────┐     ┌──────────────────┐
│   User   │ ─→  │ Django REST API  │
└──────────┘     └────────┬─────────┘
                          │
          ┌───────────────┼────────────────┐
          ▼                                ▼
 ┌────────────────┐              ┌────────────────┐
 │ ML Prediction  │              │ Sentiment NLP  │
 │ Models         │              │ News Analysis  │
 └────────────────┘              └────────────────┘
          │                                │
          └───────────────┬────────────────┘
                          ▼
                 ┌────────────────┐
                 │ Azure OpenAI   │
                 │ AI Summaries   │
                 └────────────────┘
                          │
                          ▼
                   ┌────────────┐
                   │ MySQL DB   │
                   └────────────┘
```

---

## 🧰 Tech Stack

| Category        | Technologies |
|-----------------|-------------|
| Backend         | Python 3.10, Django, Django REST Framework |
| Database        | MySQL |
| Frontend        | HTML, CSS, Bootstrap, Django Templates |
| Machine Learning| Scikit-learn, Pandas, NumPy |
| NLP             | Sentiment Analysis, Financial News Processing |
| APIs            | Alpha Vantage API, Azure OpenAI API |
| Deployment      | Docker, Docker Compose, Nginx |
| Cloud Platform  | Microsoft Azure |
| Security        | JWT Authentication, HTTPS, SSL |
| CI/CD           | GitHub Actions |

---

## 🤖 Machine Learning Pipeline

### 📈 Stock Price Prediction
Implemented multiple machine learning models to predict next-day stock prices using historical market data.

### ⚙️ Hyperparameter Optimization
Performed customized hyperparameter tuning to improve prediction accuracy and model performance.

### 📊 Model Evaluation & Comparison
Compared multiple ML algorithms using evaluation metrics such as:

- RMSE (Root Mean Squared Error)
- MAE (Mean Absolute Error)
- R² Score
- Accuracy Metrics

### 📰 Financial Sentiment Analysis
Analyzed financial news headlines and articles to generate sentiment scores influencing market trends.

### 🧠 AI-Powered Market Insights
Integrated Azure OpenAI API to generate:

- AI summaries of stock performance
- News sentiment explanations
- Market trend insights
- Simplified investor-friendly reports

---

## 📂 Core Functionalities

### 👤 Authentication System
- Secure user registration and login
- JWT token-based authentication
- Protected portfolio endpoints

### 📈 Trading Engine
- Buy/sell virtual stocks
- Simulated order execution
- Portfolio balance management

### 📊 Portfolio Analytics
- Track holdings and transaction history
- Calculate profit/loss metrics
- Daily portfolio performance logging

### 🤖 AI & Analytics Dashboard
- ML-based stock forecasting
- Sentiment score visualization
- AI-generated market summaries
- Model performance comparison dashboard

### ☁️ Deployment & DevOps
- Dockerized application services
- Azure cloud hosting
- Nginx reverse proxy configuration
- Automated deployment workflows using GitHub Actions

---

## ⚙️ Local Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/ankushp1650/zero-risk-trader.git
cd zero-risk-trader
```

---

### 2️⃣ Configure Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your_django_secret_key
DEBUG=True

DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=your_database_host

ALPHA_VANTAGE_API_KEY=your_api_key
AZURE_OPENAI_API_KEY=your_openai_key
AZURE_OPENAI_ENDPOINT=your_endpoint
```

---

### 3️⃣ Run with Docker

```bash
docker-compose build
docker-compose up
```

Application will be available at:

```text
http://localhost:8000
```

---

## 🧪 Running Tests

```bash
python manage.py test
```

---

## 🔄 CI/CD Workflow

The project uses GitHub Actions to automate:

- Build validation
- Docker image creation
- Deployment workflows
- Continuous integration checks

---

## 🔐 Security Features

- JWT-based authentication
- Environment variable protection
- HTTPS enabled using Let’s Encrypt SSL certificates
- Reverse proxy security using Nginx

---

## 📌 Future Improvements

- 📉 Deep Learning models (LSTM/Transformers)
- 📊 Interactive visualization dashboards
- ⚡ Real-time market streaming with WebSockets
- 📱 Mobile-first responsive UI
- 🤖 AI trading assistant using autonomous agents
- 📈 Portfolio risk analysis & recommendation engine

---

## 👨‍💻 Author

Ankush Patil

- AI/ML Engineer | Full Stack Developer
- Focus Areas: NLP, GenAI, Trading Systems, Data Engineering
