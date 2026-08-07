import hashlib
import time
from typing import Any, Dict


class ReasoningCache:
    """
    ULTRON Reasoning Cache

    Caches expensive LLM reasoning.

    Examples:
    - Code generation
    - Project planning
    - Code review
    - Security review
    - General chat
    """

    def __init__(self):

        self._cache: Dict[str, Dict] = {}

    # =====================================================
    # Cache Key
    # =====================================================

    def _key(self, prompt: str) -> str:

        return hashlib.sha256(

            prompt.encode("utf-8")

        ).hexdigest()

    # =====================================================
    # Store
    # =====================================================

    def store(

        self,

        prompt: str,

        response: Any,

        ttl: int = 3600

    ):

        key = self._key(prompt)

        self._cache[key] = {

            "response": response,

            "expires": time.time() + ttl,

            "created": time.time()

        }

    # =====================================================
    # Retrieve
    # =====================================================

    def get(

        self,

        prompt: str

    ):

        key = self._key(prompt)

        item = self._cache.get(key)

        if item is None:

            return None

        if time.time() > item["expires"]:

            del self._cache[key]

            return None

        return item["response"]

    # =====================================================
    # Exists
    # =====================================================

    def exists(

        self,

        prompt: str

    ) -> bool:

        return self.get(prompt) is not None

    # =====================================================
    # Remove
    # =====================================================

    def delete(

        self,

        prompt: str

    ):

        key = self._key(prompt)

        self._cache.pop(

            key,

            None

        )

    # =====================================================
    # Clear
    # =====================================================

    def clear(self):

        self._cache.clear()

    # =====================================================
    # Cleanup
    # =====================================================

    def cleanup(self):

        now = time.time()

        expired = [

            key

            for key, value in self._cache.items()

            if value["expires"] < now

        ]

        for key in expired:

            del self._cache[key]

    # =====================================================
    # Statistics
    # =====================================================

    def stats(self):

        self.cleanup()

        return {

            "cached_items": len(self._cache)

        }


reasoning_cache = ReasoningCache()