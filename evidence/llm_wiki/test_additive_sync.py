from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from evidence.llm_wiki.additive_sync import (
    EvidenceInputError,
    apply_additive_checks,
    format_log,
    load_fixture,
)


ROOT = Path(__file__).resolve().parent


class AdditiveSyncEvidenceTest(unittest.TestCase):
    def setUp(self):
        self.canonical = load_fixture("input.canonical.synthetic.json")
        self.mobile = load_fixture("input.mobile.synthetic.json")

    def test_published_after_and_trace_match_harness(self):
        after, trace = apply_additive_checks(self.canonical, self.mobile)
        self.assertEqual(load_fixture("expected.after.json"), after)
        self.assertEqual(load_fixture("trace.pass.json"), trace)

    def test_published_anonymized_log_matches_harness(self):
        _, trace = apply_additive_checks(self.canonical, self.mobile)
        expected = (ROOT / "log.anonymized.txt").read_text(encoding="utf-8")
        self.assertEqual(expected, format_log(trace))

    def test_requested_check_is_added(self):
        after, trace = apply_additive_checks(self.canonical, self.mobile)
        by_id = {item["id"]: item for item in after["items"]}
        self.assertTrue(by_id["SYN-ITEM-A"]["checked"])
        self.assertEqual(["SYN-ITEM-A"], trace["applied"])

    def test_mobile_uncheck_never_unchecks_canonical(self):
        after, trace = apply_additive_checks(self.canonical, self.mobile)
        by_id = {item["id"]: item for item in after["items"]}
        self.assertTrue(by_id["SYN-ITEM-B"]["checked"])
        self.assertEqual(["SYN-ITEM-B"], trace["preserved_checked"])
        self.assertEqual([], trace["unchecked"])

    def test_missing_mobile_item_never_deletes_canonical(self):
        after, trace = apply_additive_checks(self.canonical, self.mobile)
        self.assertIn("SYN-ITEM-C", {item["id"] for item in after["items"]})
        self.assertEqual(["SYN-ITEM-C"], trace["preserved_missing"])
        self.assertEqual([], trace["removed"])

    def test_unknown_mobile_item_is_not_inserted(self):
        after, trace = apply_additive_checks(self.canonical, self.mobile)
        self.assertNotIn("SYN-ITEM-D", {item["id"] for item in after["items"]})
        self.assertEqual(["SYN-ITEM-D"], trace["unmatched"])

    def test_matching_uses_id_not_mobile_order(self):
        reversed_mobile = copy.deepcopy(self.mobile)
        reversed_mobile["items"].reverse()
        first = apply_additive_checks(self.canonical, self.mobile)
        second = apply_additive_checks(self.canonical, reversed_mobile)
        self.assertEqual(first, second)

    def test_second_application_is_idempotent(self):
        once, _ = apply_additive_checks(self.canonical, self.mobile)
        twice, trace = apply_additive_checks(once, self.mobile)
        self.assertEqual(once, twice)
        self.assertEqual([], trace["applied"])
        self.assertEqual([], trace["removed"])
        self.assertEqual([], trace["unchecked"])

    def test_inputs_are_not_mutated(self):
        canonical_before = copy.deepcopy(self.canonical)
        mobile_before = copy.deepcopy(self.mobile)
        apply_additive_checks(self.canonical, self.mobile)
        self.assertEqual(canonical_before, self.canonical)
        self.assertEqual(mobile_before, self.mobile)

    def test_duplicate_ids_are_rejected(self):
        invalid = copy.deepcopy(self.canonical)
        invalid["items"].append(copy.deepcopy(invalid["items"][0]))
        with self.assertRaises(EvidenceInputError):
            apply_additive_checks(invalid, self.mobile)

    def test_reconstructed_trace_is_not_presented_as_verified(self):
        trace = json.loads(
            (ROOT / "trace.fail-reconstructed.json").read_text(encoding="utf-8")
        )
        self.assertEqual("Reconstructed", trace["classification"])
        self.assertFalse(trace["verified"])
        self.assertEqual("FAIL", trace["decision"])
        self.assertIn("재현이 아닙니다", trace["notice"])


if __name__ == "__main__":
    unittest.main()
