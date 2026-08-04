from app.memory.history import chat_history


class MemoryManager:

    def remember(self, user, assistant):

        chat_history.add("user", user)

        chat_history.add("assistant", assistant)

    def history(self):

        return chat_history.get()

    def clear(self):

        chat_history.clear()


memory = MemoryManager()