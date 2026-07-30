from app.core.llm import llm


def main():

    response = llm.invoke(
        "You are ULTRON. Introduce yourself in one sentence."
    )

    print("\nULTRON:")
    print(response.content)


if __name__ == "__main__":
    main()