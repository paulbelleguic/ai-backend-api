# AI Backend API

API FastAPI pour servir deux systèmes IA :

- un modèle ML de prédiction via `POST /predict`
- un assistant e-commerce hybride RAG/catalogue via `POST /chat`

## Architecture

```text
app/
├── api/routes/       # endpoints FastAPI
├── schemas/          # validation Pydantic
├── services/         # logique métier appelée par les routes
├── models/           # artefacts ML
└── rag/              # pipeline RAG, FAISS, catalogue, LLM local
```

## Lancement local

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Documentation interactive :

```text
http://127.0.0.1:8000/docs
```

## Docker

```powershell
docker build -t ai-backend-api .
docker run -p 8000:8000 ai-backend-api
```

Ou avec Compose :

```powershell
docker compose up --build
```

## Endpoints

### Health

```http
GET /health
```

### Prediction ML

```http
POST /predict
```

Exemple :

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

### Chat RAG

```http
POST /chat
```

Exemple :

```json
{
  "question": "je cherche des produits pas chers",
  "history": []
}
```

## Déploiement Render

Le fichier `render.yaml` permet de créer un Web Service Docker sur Render.

Le service expose automatiquement le port fourni par la variable `PORT`.
