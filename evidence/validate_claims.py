from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REQUIRED = {
    "id",
    "value",
    "as_of",
    "source",
    "command",
    "scope",
    "public_copy_ko",
    "public_copy_en",
    "exclusions",
    "status",
    "expires_at",
}
LOCAL_PATH = re.compile(r"(?:/[U]sers/|/h[o]me/|[A-Za-z]:\\\\U[s]ers\\\\)")
TOKEN = re.compile(r"(?:github_pat_|ghp_|AIza|sk-)[A-Za-z0-9_-]{8,}")


def load_registry() -> dict:
    return json.loads((ROOT / "claims.json").read_text(encoding="utf-8"))


def strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from strings(item)


def year_month_or_date(value: str) -> date:
    if re.fullmatch(r"\d{4}-\d{2}", value):
        value = f"{value}-01"
    return date.fromisoformat(value[:10])


def validate(registry: dict) -> list[str]:
    errors = []
    allowed_status = set(registry.get("status_values", []))
    claims = registry.get("claims", [])
    ids = [claim.get("id") for claim in claims]

    if len(ids) != len(set(ids)):
        errors.append("claim ids must be unique")

    for index, claim in enumerate(claims):
        missing = REQUIRED - set(claim)
        if missing:
            errors.append(f"claims[{index}] missing: {sorted(missing)}")
            continue
        if claim["status"] not in allowed_status:
            errors.append(f"{claim['id']}: unknown status {claim['status']}")
        if not isinstance(claim["exclusions"], list) or not claim["exclusions"]:
            errors.append(f"{claim['id']}: exclusions must be a non-empty list")
        try:
            measured = year_month_or_date(claim["as_of"])
            expires = claim["expires_at"]
            if expires and year_month_or_date(expires) < measured:
                errors.append(f"{claim['id']}: expires before as_of")
        except ValueError:
            errors.append(f"{claim['id']}: invalid date")
        for text in strings(claim):
            if LOCAL_PATH.search(text):
                errors.append(f"{claim['id']}: local absolute path found")
            if TOKEN.search(text):
                errors.append(f"{claim['id']}: token-like string found")

    return errors


def main() -> int:
    errors = validate(load_registry())
    if errors:
        print("\n".join(errors))
        return 1
    print(f"claims: OK ({len(load_registry()['claims'])} records)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
