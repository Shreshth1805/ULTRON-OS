from typing import Literal


Intent = Literal[
    "software_engineer",
    "automl",
    "general"
]


def detect_intent(message: str) -> Intent:

    text = message.lower().strip()

    automl_keywords = [
        "dataset",
        "csv",
        "automl",
        "machine learning",
        "train model",
        "train a model",
        "classification",
        "regression",
        "predict",
        "prediction",
        "accuracy",
        "f1 score",
        "feature",
        "target column"
    ]

    software_keywords = [
        "code",
        "python",
        "javascript",
        "typescript",
        "java",
        "c++",
        "bug",
        "debug",
        "function",
        "class",
        "api",
        "fastapi",
        "program",
        "script",
        "error",
        "fix this code",
        "write code"
    ]

    for keyword in automl_keywords:
        if keyword in text:
            return "automl"

    for keyword in software_keywords:
        if keyword in text:
            return "software_engineer"

    return "general"