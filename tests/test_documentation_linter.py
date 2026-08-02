from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "lint_documentation.py"
SPEC = importlib.util.spec_from_file_location("lint_documentation", MODULE_PATH)
assert SPEC and SPEC.loader
LINTER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(LINTER)


class DocumentationLinterTests(unittest.TestCase):
    def test_deprecated_term_is_reported_outside_code(self) -> None:
        policy = {
            "deprecated_terms": [
                {"pattern": r"\bhub\b", "replacement": "transit party", "reason": "Not canonical."}
            ]
        }
        findings = LINTER.check_terms(Path("documents/example.md"), "# Example\n\nA hub receives value.\n", policy)
        self.assertEqual([finding.code for finding in findings], ["TERM001"])

    def test_code_fence_does_not_define_protocol_prose(self) -> None:
        policy = {
            "deprecated_terms": [
                {"pattern": r"\bhub\b", "replacement": "transit party", "reason": "Not canonical."}
            ]
        }
        text = "# Example\n\n```text\nlegacy hub payload\n```\n"
        self.assertEqual(LINTER.check_terms(Path("documents/example.md"), text, policy), [])

    def test_broken_relative_link_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = Path("documents/example.md")
            (root / path.parent).mkdir()
            findings = LINTER.check_links(root, path, "# Example\n\n[Missing](missing.md)\n")
            self.assertEqual([finding.code for finding in findings], ["LINK002"])

    def test_one_h1_at_first_line_is_valid(self) -> None:
        findings = LINTER.check_structure(Path("documents/example.md"), "# Example\n\n## Purpose\n")
        self.assertEqual(findings, [])


if __name__ == "__main__":
    unittest.main()
