import pandas as pd


def profile_dataset(filename: str):

    df = pd.read_csv(filename)

    profile = {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "column_names": df.columns.tolist(),
        "missing_values": {
            column: int(df[column].isnull().sum())
            for column in df.columns
        },
        "data_types": {
            column: str(df[column].dtype)
            for column in df.columns
        }
    }

    return profile