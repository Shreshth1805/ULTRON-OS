from app.tools.registry import get_agent


def run_automl(
    filename: str,
    target_column: str
):
    """
    Run ULTRON's AutoML agent on a dataset.
    """

    agent = get_agent("automl_agent")

    result = agent.train(
        filename=filename,
        target_column=target_column
    )

    return result