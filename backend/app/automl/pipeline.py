from pathlib import Path

from app.automl.preprocessing import preprocess_data
from app.automl.profiler import profile_dataset
from app.automl.trainer import train_models
from app.automl.evaluator import evaluate_models


def run_automl(
    filename: str,
    target_column: str
):
    """
    Complete ULTRON AutoML pipeline.

    Steps:
    1. Load and profile dataset
    2. Preprocess dataset
    3. Train multiple models
    4. Evaluate models
    5. Return best model information
    """

    dataset_path = Path(filename)

    if not dataset_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {filename}"
        )

    # -------------------------------------------------
    # 1. PROFILE DATASET
    # -------------------------------------------------

    profile = profile_dataset(
        str(dataset_path)
    )

    # -------------------------------------------------
    # 2. PREPROCESS DATA
    # -------------------------------------------------

    X_train, X_test, y_train, y_test, task_type = preprocess_data(
        str(dataset_path),
        target_column
    )

    # -------------------------------------------------
    # 3. TRAIN MODELS
    # -------------------------------------------------

    models = train_models(
        X_train,
        y_train,
        task_type
    )

    # -------------------------------------------------
    # 4. EVALUATE
    # -------------------------------------------------

    results = evaluate_models(
        models,
        X_test,
        y_test,
        task_type
    )

    # -------------------------------------------------
    # 5. FIND BEST MODEL
    # -------------------------------------------------

    if not results:
        raise RuntimeError(
            "No models were successfully trained."
        )

    best_model_name = max(
        results,
        key=lambda name: results[name]["score"]
    )

    return {
        "status": "success",
        "task_type": task_type,
        "profile": profile,
        "results": results,
        "best_model": best_model_name,
        "best_score": results[best_model_name]["score"]
    }