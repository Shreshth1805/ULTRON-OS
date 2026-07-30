from sklearn.metrics import (
    accuracy_score,
    r2_score
)


def evaluate_models(
    models,
    X_test,
    y_test,
    task_type: str
):

    results = {}

    for name, model in models.items():

        try:

            predictions = model.predict(
                X_test
            )

            if task_type == "classification":

                score = accuracy_score(
                    y_test,
                    predictions
                )

                metric = "accuracy"

            else:

                score = r2_score(
                    y_test,
                    predictions
                )

                metric = "r2"

            results[name] = {
                "metric": metric,
                "score": float(score)
            }

        except Exception as error:

            results[name] = {
                "metric": "error",
                "score": -999,
                "error": str(error)
            }

    return results