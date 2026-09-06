from __future__ import annotations

import copy
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


class EvidenceInputError(ValueError):
    """Raised when a synthetic fixture violates the public contract."""


def _validated_items(payload: dict, label: str) -> list[dict]:
    if payload.get("data_class") != "synthetic":
        raise EvidenceInputError(f"{label}: data_class must be synthetic")
    items = payload.get("items")
    if not isinstance(items, list):
        raise EvidenceInputError(f"{label}: items must be a list")

    seen: set[str] = set()
    for item in items:
        if not isinstance(item, dict):
            raise EvidenceInputError(f"{label}: every item must be an object")
        item_id = item.get("id")
        checked = item.get("checked")
        if not isinstance(item_id, str) or not item_id.startswith("SYN-ITEM-"):
            raise EvidenceInputError(f"{label}: id must start with SYN-ITEM-")
        if item_id in seen:
            raise EvidenceInputError(f"{label}: duplicate id {item_id}")
        if not isinstance(checked, bool):
            raise EvidenceInputError(f"{label}: checked must be boolean")
        seen.add(item_id)
    return items


def apply_additive_checks(canonical: dict, mobile: dict) -> tuple[dict, dict]:
    """Apply only false-to-true check changes from a synthetic mobile copy."""
    canonical_items = _validated_items(canonical, "canonical")
    mobile_items = _validated_items(mobile, "mobile")

    before = copy.deepcopy(canonical)
    after = copy.deepcopy(canonical)
    canonical_ids = {item["id"] for item in canonical_items}
    mobile_by_id = {item["id"]: item for item in mobile_items}

    applied: list[str] = []
    preserved_checked: list[str] = []
    preserved_missing: list[str] = []

    for item in after["items"]:
        item_id = item["id"]
        mobile_item = mobile_by_id.get(item_id)
        if item["checked"]:
            if mobile_item is not None and mobile_item["checked"] is False:
                preserved_checked.append(item_id)
            continue
        if mobile_item is None:
            preserved_missing.append(item_id)
            continue
        if mobile_item["checked"]:
            item["checked"] = True
            applied.append(item_id)

    unmatched = sorted(
        item["id"] for item in mobile_items if item["id"] not in canonical_ids
    )

    _assert_additive_invariants(before, after)
    trace = {
        "classification": "Verified",
        "contract": "additive_only",
        "data_class": "synthetic",
        "decision": "PASS",
        "counts": {
            "canonical_items_before": len(before["items"]),
            "canonical_items_after": len(after["items"]),
            "mobile_items": len(mobile_items),
        },
        "applied": applied,
        "preserved_checked": preserved_checked,
        "preserved_missing": preserved_missing,
        "unmatched": unmatched,
        "removed": [],
        "unchecked": [],
    }
    return after, trace


def _assert_additive_invariants(before: dict, after: dict) -> None:
    before_items = before["items"]
    after_items = after["items"]
    if [item["id"] for item in after_items] != [item["id"] for item in before_items]:
        raise AssertionError("item identity or order changed")

    for old, new in zip(before_items, after_items, strict=True):
        old_without_check = {key: value for key, value in old.items() if key != "checked"}
        new_without_check = {key: value for key, value in new.items() if key != "checked"}
        if old_without_check != new_without_check:
            raise AssertionError(f"non-check fields changed for {old['id']}")
        if old["checked"] and not new["checked"]:
            raise AssertionError(f"checked item was unset: {old['id']}")


def format_log(trace: dict) -> str:
    counts = trace["counts"]

    def values(key: str) -> str:
        items = trace[key]
        return ",".join(items) if items else "none"

    lines = [
        "T+000ms classification=Verified data=synthetic",
        (
            "T+001ms "
            f"canonical_items={counts['canonical_items_before']} "
            f"mobile_items={counts['mobile_items']}"
        ),
        f"T+002ms applied={values('applied')}",
        f"T+003ms preserved_checked={values('preserved_checked')}",
        f"T+004ms preserved_missing={values('preserved_missing')}",
        f"T+005ms unmatched={values('unmatched')}",
        (
            "T+006ms "
            f"removed={len(trace['removed'])} "
            f"unchecked={len(trace['unchecked'])} "
            f"decision={trace['decision']}"
        ),
    ]
    return "\n".join(lines) + "\n"


def load_fixture(name: str) -> dict:
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def main() -> int:
    canonical = load_fixture("input.canonical.synthetic.json")
    mobile = load_fixture("input.mobile.synthetic.json")
    after, trace = apply_additive_checks(canonical, mobile)
    print(json.dumps({"after": after, "trace": trace}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
