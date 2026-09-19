import re
from pathlib import Path

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

class LocalKeywordRetriever:
    def retrieve(self, question: str, limit: int = 3):
        terms = set(re.findall(r"[a-zA-Z0-9_]+", question.lower()))
        results = []

        for path in DATA_DIR.glob("*.txt"):
            text = path.read_text(encoding="utf-8", errors="ignore")
            for paragraph in [p.strip() for p in text.split("\n") if p.strip()]:
                words = set(re.findall(r"[a-zA-Z0-9_]+", paragraph.lower()))
                score = len(terms.intersection(words))
                if score:
                    results.append({
                        "id": f"{path.name}:{abs(hash(paragraph))}",
                        "source": path.name,
                        "text": paragraph,
                        "score": float(score),
                        "metadata": {"source": path.name}
                    })

        results.sort(key=lambda item: item["score"], reverse=True)
        return results[:limit]
