from app.bus.broker import event_broker

from app.tools.registry import get_agent


def subscribe_defaults():

    reviewer = get_agent(
        "reviewer_agent"
    )

    if reviewer:

        event_broker.subscribe(

            "PROJECT_CREATED",

            lambda e: reviewer.review_project(
                e.payload["project_path"]
            )

        )

    tester = get_agent(
        "tester_agent"
    )

    if tester:

        event_broker.subscribe(

            "PROJECT_CREATED",

            lambda e: tester.test_project(
                e.payload["project_path"]
            )

        )

    security = get_agent(
        "security_agent"
    )

    if security:

        event_broker.subscribe(

            "PROJECT_CREATED",

            lambda e: security.review(
                e.payload["code"]
            )

        )