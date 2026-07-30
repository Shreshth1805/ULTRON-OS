# app/automl/automl.py

from app.automl.agent import automl_agent


def run_automl(
    filename: str,
    target_column: str
):

    return automl_agent.train(
        filename=filename,
        target_column=target_column
    )