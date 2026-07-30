from app.orchestration.brain import process_request


tests = [
    "Hello ULTRON",

    "Write a Python function to calculate factorial",

    "I have a CSV dataset and want to train the best machine learning model",

    "Explain how neural networks work"
]


for message in tests:

    print("\n" + "=" * 60)

    print("USER:")
    print(message)

    result = process_request(
        message
    )

    print("\nULTRON:")
    print(result)