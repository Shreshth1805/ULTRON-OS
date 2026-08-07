from datetime import datetime
from typing import List, Dict

from app.core.llm import llm
from app.memory_v2.memory_manager import memory_manager


SYSTEM_PROMPT = """
You are ULTRON's Memory Summarizer.

Your job is to summarize conversations while preserving:

- User goals
- User preferences
- Important decisions
- Code snippets mentioned
- Project progress
- Bugs encountered
- Fixes applied
- TODO items
- Follow-up actions

Keep the summary concise but complete.
"""


class ConversationSummary:

    """
    Summarizes long conversations
    for long-term memory.
    """

    # =====================================================
    # Build Conversation
    # =====================================================

    def build_text(
        self,
        history: List[Dict]
    ) -> str:

        lines = []

        for item in history:

            role = item.get(
                "role",
                "user"
            )

            message = item.get(
                "message",
                ""
            )

            lines.append(
                f"{role}: {message}"
            )

        return "\n".join(lines)

    # =====================================================
    # Summarize
    # =====================================================

    def summarize(
        self,
        history: List[Dict]
    ) -> str:

        if not history:

            return ""

        conversation = self.build_text(
            history
        )

        prompt = f"""
{SYSTEM_PROMPT}

Conversation

--------------------

{conversation}

--------------------

Produce a useful summary.
"""

        response = llm.invoke(
            prompt
        )

        return getattr(
            response,
            "content",
            str(response)
        )

    # =====================================================
    # Save Summary
    # =====================================================

    def save(
        self,
        history: List[Dict]
    ):

        summary = self.summarize(
            history
        )

        memory_manager.add(

            category="conversation_summary",

            content=summary,

            metadata={

                "created_at":
                    datetime.utcnow().isoformat(),

                "messages":
                    len(history)

            }

        )

        return summary

    # =====================================================
    # Auto Summarize
    # =====================================================

    def auto_save(
        self,
        history: List[Dict],
        threshold: int = 40
    ):

        if len(history) < threshold:

            return None

        return self.save(history)


conversation_summary = ConversationSummary()