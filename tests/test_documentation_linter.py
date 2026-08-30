# © 2026 aiaiaiai · aiaiaiai.org

from __future__ import annotations

import importlib.util
import json
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

    def test_contract_json_rejects_numeric_tokens(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "fixture.json"
            path.write_text('{"revision":1}\n', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "JSON numeric token is forbidden"):
                LINTER.load_contract_json(path)

    def test_contract_json_rejects_duplicate_members(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "fixture.json"
            path.write_text('{"version":"0.1.0","version":"0.1.0"}\n', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "duplicate JSON member"):
                LINTER.load_contract_json(path)

    def test_fixture_record_discovery_descends_into_arrays(self) -> None:
        record = {
            "contract_version": "0.1.0",
            "record_kind": "fixture.opened",
            "bch_id": "bch_example",
            "sequence": "0",
            "previous_record_hash": None,
            "actor_bond_id": "bond_example",
            "observed_at_unix_ms": "0",
            "body": {},
            "record_hash": "sha256_example",
        }
        self.assertEqual(list(LINTER.fixture_records({"history": [record]})), [record])

    def test_core_contract_digest_mismatch_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            documents = root / "documents"
            contracts = root / "contracts/core/v0"
            documents.mkdir()
            contracts.mkdir(parents=True)
            contract = documents / "19-core-client-contract.md"
            contract.write_text(
                "# Contract\n\n[Protocol Laws](00-protocol-laws.md)\n",
                encoding="utf-8",
            )
            consumer = documents / "consumer.md"
            consumer.write_text(
                "# Consumer\n\n[Contract](19-core-client-contract.md)\n",
                encoding="utf-8",
            )
            corpus = {
                "contract_version": "0.1.0",
                "fixture_corpus_version": "0.1.0",
                "production_registries": {
                    "commands": [],
                    "events": [],
                    "effects": [],
                    "projections": [],
                },
                "cases": [
                    {
                        "case_id": "example",
                        "input": {"command": {"kind": "fixture.open"}},
                        "expected": {"error": {}},
                    }
                ],
            }
            (contracts / "fixture-corpus.json").write_text(json.dumps(corpus), encoding="utf-8")
            (contracts / "fixture-corpus.sha256").write_text("sha256_invalid\n", encoding="utf-8")
            policy = {
                "core_contract": {
                    "document": "documents/19-core-client-contract.md",
                    "consumers": ["documents/consumer.md"],
                    "contract_version": "0.1.0",
                    "fixture_corpus": "contracts/core/v0/fixture-corpus.json",
                    "fixture_corpus_version": "0.1.0",
                    "fixture_digest": "contracts/core/v0/fixture-corpus.sha256",
                    "fixture_digest_domain": "0x1:core-fixture-corpus:v0",
                    "production_registry_names": ["commands", "events", "effects", "projections"],
                }
            }
            findings = LINTER.check_core_contract(root, policy)
            self.assertIn("CORE018", [finding.code for finding in findings])

    def test_core_contract_rejects_non_empty_production_registry(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            documents = root / "documents"
            contracts = root / "contracts/core/v0"
            documents.mkdir()
            contracts.mkdir(parents=True)
            (documents / "19-core-client-contract.md").write_text("# Contract\n", encoding="utf-8")
            corpus = {
                "contract_version": "0.1.0",
                "fixture_corpus_version": "0.1.0",
                "production_registries": {
                    "commands": ["message.send"],
                    "events": [],
                    "effects": [],
                    "projections": [],
                },
                "cases": [
                    {
                        "case_id": "example",
                        "input": {"command": {"kind": "fixture.open"}},
                        "expected": {"error": {}},
                    }
                ],
            }
            (contracts / "fixture-corpus.json").write_text(json.dumps(corpus), encoding="utf-8")
            digest = LINTER.prefixed_sha256("0x1:core-fixture-corpus:v0", corpus)
            (contracts / "fixture-corpus.sha256").write_text(f"{digest}\n", encoding="utf-8")
            policy = {
                "core_contract": {
                    "document": "documents/19-core-client-contract.md",
                    "consumers": [],
                    "contract_version": "0.1.0",
                    "fixture_corpus": "contracts/core/v0/fixture-corpus.json",
                    "fixture_corpus_version": "0.1.0",
                    "fixture_digest": "contracts/core/v0/fixture-corpus.sha256",
                    "fixture_digest_domain": "0x1:core-fixture-corpus:v0",
                    "production_registry_names": ["commands", "events", "effects", "projections"],
                }
            }
            findings = LINTER.check_core_contract(root, policy)
            self.assertIn("CORE010", [finding.code for finding in findings])


if __name__ == "__main__":
    unittest.main()
