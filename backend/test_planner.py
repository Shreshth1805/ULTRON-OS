from app.agents.planner.planner import planner_node


def main():

    requests = [

        "Create a FastAPI backend for my application.",

        "Train a Random Forest model using my CSV dataset.",

        "Explain how convolutional neural networks work.",

        "What is Python?"
    ]

    for request in requests:

        result = planner_node(request)

        print("\nUSER:")
        print(request)

        print("SELECTED AGENT:")
        print(result)


if __name__ == "__main__":
    main()