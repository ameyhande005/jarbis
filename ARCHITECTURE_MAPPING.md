# Architecture Mapping

| Architecture concept | Prototype location |
|---|---|
| Web interface | `app/static/index.html` |
| API/backend | `app/main.py` |
| Policy check | `app/policy.py` |
| Moss retrieval adapter | `app/moss_retriever.py` |
| Local fallback retrieval | `app/local_retriever.py` |
| Moss index creation | `scripts/build_moss_index.py` |
| Audit logging | `app/audit.py` |
| Feedback loop | `/feedback` endpoint |
| Local document area | `data/` |

The architecture diagram supplied for this project is visually dense and its labels could not be reliably extracted from the PDF. This repository therefore implements the central retrieval, policy, audit, and feedback concepts while explicitly marking advanced enterprise controls as future work.
