from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from evidence.content_automation.validator import evaluate


ROOT = Path(__file__).resolve().parent


def load(name: str) -> dict:
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


class ContentAutomationEvidenceTest(unittest.TestCase):
    def setUp(self):
        self.approved = load("input.approved.json")

    def assert_block(self, payload: dict, code: str):
        result = evaluate(payload)
        self.assertEqual("BLOCK", result["decision"])
        self.assertEqual("NONE", result["next_stage"])
        self.assertIn(code, {item["code"] for item in result["issues"]})

    def test_published_examples_match_expected_results(self):
        self.assertEqual(load("expected.blocked.json"), evaluate(load("input.blocked.json")))
        self.assertEqual(load("expected.approved.json"), evaluate(self.approved))

    def test_manifest_separates_observed_reconstructed_and_verified(self):
        manifest = load("manifest.json")
        self.assertEqual("synthetic", manifest["data_class"])
        self.assertEqual(
            ["Observed", "Reconstructed", "Verified"],
            [item["classification"] for item in manifest["evidence"]],
        )

    def test_subject_alignment_blocks(self):
        case = copy.deepcopy(self.approved)
        case["draft"]["subject"] = "SAMPLE-B"
        self.assert_block(case, "subject_mismatch")

    def test_number_grounding_blocks(self):
        self.assert_block(load("input.blocked.json"), "source_number_mismatch")

    def test_direction_consistency_blocks(self):
        case = copy.deepcopy(self.approved)
        case["draft"]["direction"] = "down"
        self.assert_block(case, "direction_mismatch")

    def test_source_attribution_blocks(self):
        case = copy.deepcopy(self.approved)
        case["draft"]["source_id"] = "EXAMPLE-SOURCE-999"
        self.assert_block(case, "source_id_mismatch")

    def test_as_of_alignment_blocks(self):
        case = copy.deepcopy(self.approved)
        case["draft"]["as_of"] = "2026-09-05"
        self.assert_block(case, "as_of_mismatch")

    def test_prohibited_advice_blocks(self):
        case = copy.deepcopy(self.approved)
        case["draft"]["body"] = "지금 매수하세요."
        self.assert_block(case, "unsafe_advice")

    def test_presentation_warning_does_not_block(self):
        case = copy.deepcopy(self.approved)
        case["draft"]["title"] = "긴 제목 " * 20
        result = evaluate(case)
        self.assertEqual("PASS", result["decision"])
        self.assertIn("title_too_long", {item["code"] for item in result["issues"]})

    def test_human_approval_blocks_private_upload(self):
        case = copy.deepcopy(self.approved)
        case["draft"]["human_approved"] = False
        self.assert_block(case, "approval_missing")
