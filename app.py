import csv
import math
from pathlib import Path

from fastapi import FastAPI, HTTPException

app = FastAPI(
    title="HELIOS Task Duration Predictor",
    description="Predicts task duration range by task type based on pre-computed model results.",
    version="1.0.0",
)

CSV_PATH = Path(__file__).parent / "task_type_predictions.csv"


def _load_predictions(path: Path) -> dict:
    predictions = {}
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            predictions[row["task_type"]] = {
                "predicted_mean": float(row["predicted_mean"]),
                "error": float(row["error"]),
            }
    return predictions


PREDICTIONS = _load_predictions(CSV_PATH)

KEYWORD_MAP = {
    "removal": "Removal / Installation",
    "installation": "Removal / Installation",
    "install": "Removal / Installation",
    "remove": "Removal / Installation",
    "cleaning": "Cleaning",
    "clean": "Cleaning",
    "inspection": "Inspection / Check",
    "inspect": "Inspection / Check",
    "check": "Inspection / Check",
    "test": "Tests",
    "tests": "Tests",
}


def _classify_task(task_name: str) -> str | None:
    lower = task_name.lower()
    # Try exact match first
    for task_type in PREDICTIONS:
        if task_type.lower() == lower:
            return task_type
    # Try keyword match
    for keyword, task_type in KEYWORD_MAP.items():
        if keyword in lower:
            return task_type
    # Default: anything unmatched is a special procedure
    return "Special Procedure"


def _duration_range(predicted_mean: float, error: float) -> tuple[int, int]:
    min_days = math.ceil(predicted_mean)
    max_days = math.ceil(predicted_mean + error)
    return min_days, max_days


@app.get("/predict/{task_name:path}")
def predict(task_name: str):
    task_type = _classify_task(task_name)
    if task_type is None:
        raise HTTPException(
            status_code=404,
            detail=f"Could not classify '{task_name}'. Use /task-types to see valid categories.",
        )
    entry = PREDICTIONS[task_type]
    min_days, max_days = _duration_range(entry["predicted_mean"], entry["error"])
    return {
        "task_name": task_name,
        "task_type": task_type,
        "predicted_days": min_days,
        "max_days": max_days,
        "message": f"This task may take approximately {min_days} days" if min_days == max_days else f"This task may take approximately {min_days}-{max_days} days",
    }


@app.get("/task-types")
def task_types():
    return {"task_types": list(PREDICTIONS.keys())}


@app.get("/health")
def health():
    return {"status": "ok"}
