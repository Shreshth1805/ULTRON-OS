from app.tools.registry import (
    get_agent
)


def main():

    agent = get_agent("automl")

    print(
        "Agent loaded:",
        agent.name
    )


if __name__ == "__main__":
    main()