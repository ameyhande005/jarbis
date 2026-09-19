# Prototype Feedback

## Test questions
1. Was document upload easy to understand?
2. Did retrieval return relevant passages?
3. Was the answer understandable?
4. Did the policy check block unsafe example requests?
5. Was the displayed retrieval mode clear?
6. What should be improved first?

## Record
- Tester role:
- Question:
- Retrieval mode: Moss / local fallback
- Retrieval latency shown:
- Rating (1–5):
- Security concern:
- Improvement suggestion:

## Known limitations
- The Moss integration uses the official SDK pattern and requires valid credentials.
- The current answer is extractive; a local LLM is not connected.
- The demo role selector is not real authentication.
- Permission metadata is illustrative and not yet enforced end-to-end.
- Audit logs are local JSONL and are not tamper-resistant.
