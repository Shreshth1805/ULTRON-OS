from sklearn.ensemble import (
    RandomForestClassifier,
    RandomForestRegressor,
    GradientBoostingClassifier,
    GradientBoostingRegressor
)

from sklearn.linear_model import (
    LogisticRegression,
    LinearRegression
)


def train_models(
    X_train,
    y_train,
    task_type: str
):

    models = {}

    if task_type == "classification":

        models = {
            "logistic_regression": LogisticRegression(
                max_iter=1000
            ),

            "random_forest": RandomForestClassifier(
                n_estimators=100,
                random_state=42
            ),

            "gradient_boosting": GradientBoostingClassifier(
                random_state=42
            )
        }

    else:

        models = {
            "linear_regression": LinearRegression(),

            "random_forest": RandomForestRegressor(
                n_estimators=100,
                random_state=42
            ),

            "gradient_boosting": GradientBoostingRegressor(
                random_state=42
            )
        }

    trained_models = {}

    for name, model in models.items():

        try:

            model.fit(
                X_train,
                y_train
            )

            trained_models[name] = model

        except Exception as error:

            print(
                f"Could not train {name}: {error}"
            )

    return trained_models