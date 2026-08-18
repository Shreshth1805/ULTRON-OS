from langchain_core.messages import HumanMessage
from app.core.llm import llm
from app.memory.manager import memory_manager


class ChatAgent:

    def __init__(self):
        self.name = "chat_agent"

    def chat(
        self,
        session_id: str,
        message: str
    ):

        history = memory_manager.get_history(
            session_id
        )

        messages = []

        # Add previous conversation
        for item in history:

            if item["role"] == "user":

                messages.append(
                    HumanMessage(
                        content=item["content"]
                    )
                )

            elif item["role"] == "assistant":

                from langchain_core.messages import AIMessage

                messages.append(
                    AIMessage(
                        content=item["content"]
                    )
                )

        # Add current message
        messages.append(
            HumanMessage(
                content=message
            )
        )

        response = llm.invoke(
            messages
        )

        answer = response.content

        # Save conversation
        memory_manager.add_message(
            session_id=session_id,
            role="user",
            content=message
        )

        memory_manager.add_message(
            session_id=session_id,
            role="assistant",
            content=answer
        )

        return {
            "session_id": session_id,
            "response": answer,
            "history_length": len(
                memory_manager.get_history(
                    session_id
                )
            )
        }


chat_agent = ChatAgent()