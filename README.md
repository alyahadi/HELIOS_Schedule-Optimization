# HELIOS Task Duration Estimation

A FastAPI application that predicts maintenance task duration based on pre-computed machine learning model results.

## How It Works

1. **Predictive modeling** (offline) — Jupyter notebooks train a model on historical maintenance data and export predictions to `task_type_predictions.csv`.
2. **API** (runtime) — `app.py` reads the CSV and serves duration predictions via REST endpoints.

### Task Classification

The API accepts free-text task names entered by user and classifies them into one of five task types using keyword matching:

| Keyword | Task Type |
|---|---|
| removal, remove, installation, install | Removal / Installation |
| cleaning, clean | Cleaning |
| inspection, inspect, check | Inspection / Check |
| test, tests | Tests |
| *(anything else)* | Special Procedure |

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/predict/{task_name}` | Predict duration for a task name |
| GET | `/task-types` | List all valid task type categories |
| GET | `/health` | Health check |
| GET | `/docs` | Interactive API documentation (Swagger UI) |

### Example

```
GET /predict/Remove engine cowling
```

```json
{
  "task_name": "HMU Installation",
  "task_type": "Removal / Installation",
  "predicted_days": 3,
  "max_days": 8,
  "message": "This task may take approximately 3-8 days"
}
```

## Setup

### Run locally

```bash
pip install -r requirements.txt
uvicorn app:app --host localhost --port 8000
```

### Run with Docker

```bash
docker compose up --build
```

The API will be available at `http://localhost:8000`.

## Project Structure

```
├── app.py                              # FastAPI application
├── Combined_All_Years_With_SumUp.xslx  # Historical dataset from 2013 to 2025
├── task_type_predictions.csv           # Pre-computed model predictions
├── predictive_modeling_tasks.ipynb     # Model training notebook
├── preprocess_all.ipynb                # Data preprocessing notebook
├── requirements.txt                    # Python dependencies
├── Dockerfile
├── docker-compose.yml
└── .dockerignore
```
