def check_query_policy(question: str, user_role: str):
    blocked_terms = {"delete", "drop database", "exfiltrate", "steal password"}
    normalized = question.lower()

    if any(term in normalized for term in blocked_terms):
        return False, "The request was blocked by the prototype policy check."

    if user_role not in {"employee", "manager", "admin"}:
        return False, "Unknown role. Request denied."

    return True, "Request allowed by prototype policy."
