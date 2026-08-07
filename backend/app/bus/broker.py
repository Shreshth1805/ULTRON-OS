from collections import defaultdict


class EventBroker:

    def __init__(self):

        self.listeners = defaultdict(list)

    def subscribe(
        self,
        event_type,
        callback
    ):

        self.listeners[event_type].append(
            callback
        )

    def publish(
        self,
        event
    ):

        callbacks = self.listeners.get(
            event.type,
            []
        )

        results = []

        for cb in callbacks:

            try:

                results.append(
                    cb(event)
                )

            except Exception as e:

                results.append(
                    {
                        "success": False,
                        "error": str(e)
                    }
                )

        return results


event_broker = EventBroker()