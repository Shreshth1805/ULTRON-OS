from collections import defaultdict

from app.communication.event import Event


class AgentBus:

    def __init__(self):

        self.listeners = defaultdict(list)

    # ====================================================
    # Subscribe
    # ====================================================

    def subscribe(

        self,

        event_name,

        callback

    ):

        self.listeners[event_name].append(
            callback
        )

    # ====================================================
    # Publish
    # ====================================================

    def publish(

        self,

        event_name,

        event: Event

    ):

        callbacks = self.listeners.get(
            event_name,
            []
        )

        responses = []

        for callback in callbacks:

            try:

                responses.append(
                    callback(event)
                )

            except Exception as e:

                responses.append({

                    "success": False,

                    "error": str(e)

                })

        return responses

    # ====================================================
    # Remove Listener
    # ====================================================

    def unsubscribe(

        self,

        event_name,

        callback

    ):

        if callback in self.listeners.get(
            event_name,
            []
        ):

            self.listeners[event_name].remove(
                callback
            )

    # ====================================================
    # Clear
    # ====================================================

    def clear(self):

        self.listeners.clear()

    # ====================================================
    # Stats
    # ====================================================

    def registered_events(self):

        return {

            event: len(callbacks)

            for event, callbacks

            in self.listeners.items()

        }


agent_bus = AgentBus()