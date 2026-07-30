from app.orchestration.routing import route_request


requests = [
    "Train a Random Forest model on my dataset",
    "Write a FastAPI authentication system",
    "Explain quantum computing",
    "Find research papers about transformers",
    "Hello ULTRON"
]


for request in requests:

    result = route_request(request)

    print("\nUSER:")
    print(request)

    print("ROUTE:")
    print(result.route)

    print("REASON:")
    print(result.reason)