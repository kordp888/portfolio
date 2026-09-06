from __future__ import annotations


ADVICE_PHRASES = ("매수하세요", "매도하세요", "무조건 오릅니다")
MAX_TITLE_CHARS = 60


def issue(category: str, severity: str, code: str) -> dict:
    return {"category": category, "severity": severity, "code": code}


def evaluate(payload: dict) -> dict:
    source = payload["source"]
    draft = payload["draft"]
    issues = []

    if draft["subject"] != source["subject"]:
        issues.append(issue("subject_alignment", "block", "subject_mismatch"))
    if draft["change_pct"] != source["change_pct"]:
        issues.append(issue("number_grounding", "block", "source_number_mismatch"))
    if draft["direction"] != source["direction"]:
        issues.append(issue("direction_consistency", "block", "direction_mismatch"))
    if draft["source_id"] != source["source_id"]:
        issues.append(issue("source_attribution", "block", "source_id_mismatch"))
    if draft["as_of"] != source["as_of"]:
        issues.append(issue("as_of_alignment", "block", "as_of_mismatch"))
    if any(phrase in draft["body"] for phrase in ADVICE_PHRASES):
        issues.append(issue("prohibited_advice", "block", "unsafe_advice"))
    if len(draft["title"]) > MAX_TITLE_CHARS:
        issues.append(issue("presentation_length", "warn", "title_too_long"))
    if not draft.get("human_approved", False):
        issues.append(issue("human_approval", "block", "approval_missing"))

    blocked = any(item["severity"] == "block" for item in issues)
    return {
        "decision": "BLOCK" if blocked else "PASS",
        "next_stage": "NONE" if blocked else "PRIVATE_UPLOAD",
        "issues": issues,
    }
