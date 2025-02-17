# Stock Analyzer Backend

A FastAPI-based backend service for analyzing A-shares stocks using technical indicators and industry sentiment analysis.

## Features

- Real-time stock data retrieval using akshare
- Technical analysis with multiple indicators (MA, MACD, KDJ)
- Industry sentiment analysis with OpenAI integration (optional)
- Industry theme and sector rotation tracking
- Configurable stock screening with TopK recommendations

## Setup

1. Install dependencies:
```bash
poetry install
```

2. Configure environment variables:
Copy `.env.example` to `.env` and set your configuration:
```bash
cp .env.example .env
# Edit .env to set OpenAI API key if needed
```

3. Run the server:
```bash
poetry run uvicorn app.main:app --reload
```

## API Endpoints

- `GET /api/stock/list` - Get list of A-shares stocks
- `GET /api/stock/daily/{stock_code}` - Get daily stock data
- `GET /api/stock/realtime/{stock_code}` - Get realtime stock quotes
- `POST /api/stock/screening` - Screen stocks based on technical and industry analysis

## Testing

Run tests with:
```bash
poetry run pytest tests/ -v
```

## Configuration

- `APP_ENABLE_OPENAI`: Toggle OpenAI analysis service (default: true)
- `APP_OPENAI_API_KEY`: OpenAI API key for sentiment analysis

## Development

The project uses:
- FastAPI for the web framework
- akshare for market data
- pandas for data analysis
- OpenAI for industry sentiment (optional)
