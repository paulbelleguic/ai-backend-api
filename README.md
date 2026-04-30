# AI Backend API

Production-oriented AI backend built with FastAPI.

It exposes two AI services:

- an ML prediction model through `POST /predict`
- a hybrid e-commerce RAG/catalog assistant through `POST /chat`

Live API:

```text
https://ai-backend-api-3jn5.onrender.com
```

## Architecture

```text
app/
├── api/routes/       # FastAPI endpoints
├── schemas/          # Pydantic validation
├── services/         # business logic called by routes
├── models/           # ML artifacts
└── rag/              # RAG pipeline, FAISS, catalog, local LLM

frontend/
└── streamlit_app.py  # portfolio UI consuming the deployed API
```

The API layer stays thin: routes validate HTTP payloads, schemas define input/output contracts, and services call the ML or RAG pipelines.

## Local API

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Interactive documentation:

```text
http://127.0.0.1:8000/docs
```

## Portfolio UI

The Streamlit UI calls the deployed FastAPI backend by default.

```powershell
pip install -r frontend/requirements.txt
streamlit run frontend/streamlit_app.py
```

To target a local backend:

```powershell
$env:API_URL="http://127.0.0.1:8000"
streamlit run frontend/streamlit_app.py
```

## Docker

```powershell
docker build -t ai-backend-api .
docker run -p 8000:8000 ai-backend-api
```

Or with Compose:

```powershell
docker compose up --build
```

## Endpoints

### Health

```http
GET /health
```

### ML Prediction

```http
POST /predict
```

Example:

```json
{
  "purchase_month": 5,
  "purchase_dayofweek": 2,
  "customer_state": "SP",
  "customer_city": "sao paulo",
  "payment_installments": 3,
  "items_count": 2,
  "freight_value": 21.5,
  "review_score": 4.0,
  "delivery_delay_days": 0
}
```

### RAG Chat

```http
POST /chat
```

Example:

```json
{
  "question": "je cherche des produits pas chers",
  "history": []
}
```

## Render Deployment

`render.yaml` defines the Docker web service.

The API binds to the `PORT` environment variable provided by Render.

## Tests

```powershell
pytest
```
