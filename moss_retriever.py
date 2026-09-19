import os
from pathlib import Path

class MossRetriever:
    """Optional Moss retrieval adapter.

    Moss credentials are read from environment variables.
    The SDK is initialized only when both values are present.
    """

    def __init__(self):
        self.project_id = os.getenv("MOSS_PROJECT_ID")
        self.project_key = os.getenv("MOSS_PROJECT_KEY")
        self.index_name = os.getenv("MOSS_INDEX_NAME", "sovereign-workbench")
        self.client = None
        self.enabled = bool(self.project_id and self.project_key)

        if self.enabled:
            from moss import MossClient
            self.client = MossClient(self.project_id, self.project_key)

    async def query(self, question: str, top_k: int = 3):
        if not self.enabled:
            return None

        from moss import QueryOptions
        await self.client.load_index(self.index_name)
        result = await self.client.query(
            self.index_name,
            question,
            QueryOptions(top_k=top_k)
        )

        return {
            "time_taken_ms": getattr(result, "time_taken_ms", None),
            "results": [
                {
                    "id": getattr(doc, "id", ""),
                    "source": (getattr(doc, "metadata", {}) or {}).get("source", "moss"),
                    "text": getattr(doc, "text", ""),
                    "score": float(getattr(doc, "score", 0.0)),
                    "metadata": getattr(doc, "metadata", {}) or {}
                }
                for doc in result.docs
            ]
        }
