from collections import deque


class ChatHistory:

    def __init__(self, max_messages=20):
        self.messages = deque(maxlen=max_messages)

    def add(self, role, content):
        self.messages.append({
            "role": role,
            "content": content
        })

    def get(self):
        return list(self.messages)

    def clear(self):
        self.messages.clear()


chat_history = ChatHistory()