import pandas as pd


def analyse_dataset(filename: str):

    try:

        df = pd.read_csv(filename)

        return {
            "success": True,
            "filename": filename,
            "rows": int(df.shape[0]),
            "columns": int(df.shape[1]),
            "column_names": df.columns.tolist(),
            "data_types": {
                column: str(dtype)
                for column, dtype in df.dtypes.items()
            },
            "missing_values": {
                column: int(value)
                for column, value in df.isnull().sum().items()
            }
        }

    except FileNotFoundError:

        return {
            "success": False,
            "error": f"Dataset not found: {filename}"
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }


DATASET_TOOLS = {
    "analyse_dataset": analyse_dataset
}