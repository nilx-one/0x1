from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "lint_documentation.py"
SPEC = importlib.util.spec_from_file_location("lint_documentation", MODULE_PATH)
assert SPEC and SPEC.loader
LINTER = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = LINTER
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

    def test_missing_foundation_document_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            policy = {"foundation_document": "documents/00-protocol-laws.md", "foundation_consumers": []}
            findings = LINTER.check_foundation(Path(directory), policy)
            self.assertEqual([finding.code for finding in findings], ["DOC007"])

    def test_required_consumer_must_link_to_foundation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            documents = root / "documents"
            documents.mkdir()
            (documents / "00-protocol-laws.md").write_text("# Protocol Laws\n", encoding="utf-8")
            (documents / "README.md").write_text("# Index\n", encoding="utf-8")
            policy = {
                "foundation_document": "documents/00-protocol-laws.md",
                "foundation_consumers": ["documents/README.md"],
            }
            findings = LINTER.check_foundation(root, policy)
            self.assertEqual([finding.code for finding in findings], ["DOC009"])

    def test_foundation_link_satisfies_consumer_contract(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            documents = root / "documents"
            documents.mkdir()
            (documents / "00-protocol-laws.md").write_text("# Protocol Laws\n", encoding="utf-8")
            (documents / "README.md").write_text(
                "# Index\n\n[Protocol Laws](00-protocol-laws.md)\n", encoding="utf-8"
            )
            policy = {
                "foundation_document": "documents/00-protocol-laws.md",
                "foundation_consumers": ["documents/README.md"],
            }
            self.assertEqual(LINTER.check_foundation(root, policy), [])

    def test_reading_order_must_begin_with_protocol_laws(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            documents = root / "documents"
            documents.mkdir()
            (documents / "README.md").write_text(
                "# Index\n\n1. [Glossary](02-glossary.md)\n2. [Protocol Laws](00-protocol-laws.md)\n",
                encoding="utf-8",
            )
            policy = {"required_foundation_links": ["00-protocol-laws.md", "02-glossary.md"]}
            findings = LINTER.check_index(root, policy)
            self.assertEqual([finding.code for finding in findings], ["DOC010"])

    def test_missing_document_from_canonical_sequence_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            documents = root / "documents"
            documents.mkdir()
            (documents / "README.md").write_text("# Index\n", encoding="utf-8")
            policy = {"ordered_documents": ["documents/00-protocol-laws.md"]}
            findings = LINTER.check_catalog(root, policy)
            self.assertEqual([finding.code for finding in findings], ["DOC011", "DOC013"])

    def test_unnumbered_document_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            documents = root / "documents"
            documents.mkdir()
            (documents / "README.md").write_text(
                "# Index\n\n[Protocol Laws](00-protocol-laws.md)\n", encoding="utf-8"
            )
            (documents / "00-protocol-laws.md").write_text("# Protocol Laws\n", encoding="utf-8")
            (documents / "glossary.md").write_text("# Glossary\n", encoding="utf-8")
            policy = {"ordered_documents": ["documents/00-protocol-laws.md"]}
            findings = LINTER.check_catalog(root, policy)
            self.assertEqual([finding.code for finding in findings], ["DOC012"])

    def test_index_must_follow_canonical_numeric_sequence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            documents = root / "documents"
            documents.mkdir()
            (documents / "README.md").write_text(
                "# Index\n\n[Glossary](01-glossary.md)\n[Protocol Laws](00-protocol-laws.md)\n",
                encoding="utf-8",
            )
            (documents / "00-protocol-laws.md").write_text("# Protocol Laws\n", encoding="utf-8")
            (documents / "01-glossary.md").write_text("# Glossary\n", encoding="utf-8")
            policy = {
                "ordered_documents": [
                    "documents/00-protocol-laws.md",
                    "documents/01-glossary.md",
                ]
            }
            findings = LINTER.check_catalog(root, policy)
            self.assertEqual([finding.code for finding in findings], ["DOC014"])


if __name__ == "__main__":
    unittest.main()
