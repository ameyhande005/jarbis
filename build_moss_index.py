import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

async def main():
    project_id = os.getenv("MOSS_PROJECT_ID")
    project_key = os.getenv("MOSS_PROJECT_KEY")
    index_name = os.getenv("MOSS_INDEX_NAME", "sovereign-workbench")

    if not project_id or not project_key:
        raise SystemExit("Set MOSS_PROJECT_ID and MOSS_PROJECT_KEY in .env first.")

    from moss import MossClient

    docs = []
    for path in Path("data").glob("*.txt"):
        text = path.read_text(encoding="utf-8", errors="ignore")
        paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
        for number, paragraph in enumerate(paragraphs, start=1):
            docs.append({
                "id": f"{path.name}:{number}",
                "text": paragraph,
                "metadata": {
                    "source": path.name,
                    "access_level": "employee"
                }
            })

    if not docs:
        raise SystemExit("No .txt documents found in data/.")

    client = MossClient(project_id, project_key)
    await client.create_index(index_name, docs)
    await client.load_index(index_name)
    print(f"Indexed {len(docs)} passages in Moss index '{index_name}'.")

if __name__ == "__main__":
    asyncio.run(main())
