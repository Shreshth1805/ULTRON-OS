from app.bus.broker import event_broker


class Dispatcher:

    def emit(

        self,

        event

    ):

        return event_broker.publish(
            event
        )


dispatcher = Dispatcher()