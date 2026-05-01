# AI Backend API

Production-oriented AI backend built with FastAPI.

It exposes two AI services:

- an ML order-value prediction service through `POST /predict`
- an e-commerce assistant service through `POST /chat`

Live API:

```text
https://ai-backend-api-3jn5.onrender.com
```

Interactive docs:

```text
https://ai-backend-api-3jn5.onrender.com/docs
```

## Architecture

```text
app/
├── api/routes/       # FastAPI endpoints
├── schemas/          # Pydantic input/output contracts
├── services/         # production service layer
├── models/           # ML artifacts
└── rag/              # catalog, routing, FAQ/RAG modules

frontend/
└── streamlit_app.py  # small portfolio UI consuming the API
```

The API layer stays thin: routes handle HTTP, schemas validate payloads, and services call the ML or assistant logic.

## Production Notes

The original local RAG project uses FAISS, embeddings, and a local Transformers model. For the deployed Render service, `/chat` uses a lightweight production path:

- catalog questions are answered from `products.csv`
- support questions are answered from `faq.txt`
- no heavy model is loaded at request time

This keeps the deployed demo stable on a small Render instance while preserving the same API contract.

## Local API

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Local docs:

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
POST /predict/
```

Example:

```json
{
  "purchase_year": 2019,
  "purchase_month": 5,
  "purchase_day": 15,
  "purchase_hour": 12,
  "purchase_dayofweek": 2,
  "customer_state": "SP",
  "n_items": 2,
  "n_unique_products": 2,
  "n_unique_sellers": 1,
  "payment_installments_max": 3
}
```

Response:

```json
{
  "prediction": 100.39
}
```

### E-commerce Chat

```http
POST /chat/
```

Example:

```json
{
  "question": "sneakers noires en 42",
  "history": []
}
```

Response:

```json
{
  "answer": "J'ai trouve les produits suivants : ...",
  "route": "catalog",
  "sources": ["data/raw/products.csv"]
}
```

## Render Deployment

`render.yaml` defines the Docker web service.

The API binds to the `PORT` environment variable provided by Render.

## Tests

```powershell
pytest
```
