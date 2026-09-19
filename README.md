# Sovereign On-Premise Agentic AI Workbench — Moss Prototype

This prototype demonstrates a document Q&A workflow with:
- Moss-powered semantic retrieval when Moss credentials are configured
- A local keyword-retrieval fallback for offline development
- Basic policy checks
- Local audit logging
- User feedback capture

## Important architecture note
Moss uses a project ID and project key. According to the public Moss quickstart, indexes are created/managed through Moss Cloud and then loaded into the application runtime. Therefore, this prototype does **not** claim that the entire Moss ingestion path is air-gapped or fully sovereign. Validate your deployment and data requirements before making that claim.

## Setup

Use Python 3.10+.

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file from `.env.example` and add your Moss credentials:

```env
MOSS_PROJECT_ID=your_project_id
MOSS_PROJECT_KEY=your_project_key
MOSS_INDEX_NAME=sovereign-workbench
```

Start the API:

```bash
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000

## Moss indexing

Run this once after adding or editing text documents:

```bash
python scripts/build_moss_index.py
```

The script uploads the sample text passages to the configured Moss index. Do not upload confidential documents until you have reviewed Moss's data handling, tenancy, retention, and compliance terms.

## Demo
1. Configure credentials or use fallback mode.
2. Build the Moss index.
3. Upload a `.txt` document.
4. Ask a question.
5. Review the source passages and retrieval latency.
6. Submit feedback.
7. Open `/audit` to inspect local audit events.

## Honest implementation status
Implemented:
- Optional Moss SDK retrieval
- Local fallback retrieval
- Basic policy check
- Local audit events
- Feedback endpoint

Not implemented:
- Production authentication/SSO
- Full RBAC/ABAC
- Encryption key management
- Malware scanning
- Hardened sandboxing
- Local LLM inference
- Complete production threat protections
