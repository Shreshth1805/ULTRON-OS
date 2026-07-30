import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


def preprocess_data(
    filename: str,
    target_column: str
):

    df = pd.read_csv(filename)

    if target_column not in df.columns:
        raise ValueError(
            f"Target column '{target_column}' "
            f"not found in dataset."
        )

    # Remove rows containing missing values
    df = df.dropna()

    X = df.drop(columns=[target_column])
    y = df[target_column]

    # -------------------------------------------------
    # Encode categorical features
    # -------------------------------------------------

    for column in X.select_dtypes(
        include=["object", "category"]
    ).columns:

        encoder = LabelEncoder()

        X[column] = encoder.fit_transform(
            X[column].astype(str)
        )

    # -------------------------------------------------
    # Encode target if categorical
    # -------------------------------------------------

    if (
        y.dtype == "object"
        or str(y.dtype) == "category"
    ):

        target_encoder = LabelEncoder()

        y = target_encoder.fit_transform(
            y.astype(str)
        )

        task_type = "classification"

    else:

        # Determine classification vs regression
        if y.nunique() <= 20:
            task_type = "classification"
        else:
            task_type = "regression"

    # -------------------------------------------------
    # Split
    # -------------------------------------------------

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    return (
        X_train,
        X_test,
        y_train,
        y_test,
        task_type
    )   