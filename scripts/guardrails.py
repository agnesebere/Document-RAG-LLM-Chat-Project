SENSITIVE_KEYWORDS = [
    "fraud",
    "stolen card",
    "stolen debit card",
    "stolen credit card",
    "unauthorized transaction",
    "unauthorized charge",
    "identity theft",
    "account frozen",
    "account freeze",
    "legal complaint",
    "regulatory complaint",
    "scam",
    "phishing"
]

OUT_OF_SCOPE_KEYWORDS = [
    "stock to buy",
    "which stock",
    "crypto",
    "bitcoin",
    "investment advice",
    "tax advice",
    "legal advice",
    "lawsuit",
    "medical advice"
]


def is_sensitive_query(query: str) -> bool:
    query_lower = query.lower()
    return any(keyword in query_lower for keyword in SENSITIVE_KEYWORDS)


def is_out_of_scope_query(query: str) -> bool:
    query_lower = query.lower()
    return any(keyword in query_lower for keyword in OUT_OF_SCOPE_KEYWORDS)


def fallback_response() -> str:
    return (
        "I don’t have enough information in the SecureBank knowledge base to answer that. "
        "Please contact SecureBank customer support for further assistance."
    )


def escalation_response() -> str:
    return (
        "This issue may require direct assistance from SecureBank support. "
        "Please contact SecureBank customer service or the appropriate SecureBank support team immediately."
    )


def out_of_scope_response() -> str:
    return (
        "I can only help with SecureBank products, policies, and customer support topics. "
        "I’m not able to provide advice on that request."
    )