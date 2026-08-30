#!/usr/bin/env python3
# © 2026 aiaiaiai · aiaiaiai.org
"""Validate 0x1 documentation structure, foundation, links, style, and terminology."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class Finding:
    path: Path
    line: int
    code: str
    message: str

    def github(self) -> str:
        return f"::error file={self.path},line={self.line},title={self.code}::{self.message}"


def load_policy(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def markdown_files(root: Path, policy: dict) -> list[Path]:
    excluded = {Path(value) for value in policy.get("excluded_paths", [])}
    result: set[Path] = set()
    for value in policy["roots"]:
        candidate = root / value
        if candidate.is_file() and candidate.suffix == ".md":
            result.add(candidate.relative_to(root))
        elif candidate.is_dir():
            result.update(path.relative_to(root) for path in candidate.rglob("*.md"))
    return sorted(result - excluded)


def prose_lines(text: str) -> Iterable[tuple[int, str]]:
    in_fence = False
    fence = ""
    for number, line in enumerate(text.splitlines(), start=1):
        match = re.match(r"\s*(```+|~~~+)", line)
        if match:
            marker = match.group(1)[0]
            if not in_fence:
                in_fence, fence = True, marker
            elif marker == fence:
                in_fence, fence = False, ""
            continue
        if not in_fence:
            yield number, line


def without_inline_code(line: str) -> str:
    return re.sub(r"`[^`]*`", "", line)


def check_structure(path: Path, text: str) -> list[Finding]:
    findings: list[Finding] = []
    lines = text.splitlines()
    h1 = [number for number, line in enumerate(lines, start=1) if line.startswith("# ")]
    if len(h1) != 1:
        findings.append(Finding(path, 1, "DOC001", "Markdown documents must contain exactly one H1 heading."))
    elif h1[0] != 1:
        findings.append(Finding(path, h1[0], "DOC002", "The H1 heading must be the first line."))
    for number, line in enumerate(lines, start=1):
        trailing_spaces = len(line) - len(line.rstrip(" "))
        if trailing_spaces not in (0, 2):
            findings.append(Finding(path, number, "DOC003", "Trailing spaces are forbidden except the two-space Markdown line break."))
        if "\t" in line:
            findings.append(Finding(path, number, "DOC004", "Tabs are not allowed in Markdown."))
        if re.match(r"^#{1,6}[^ #]", line):
            findings.append(Finding(path, number, "DOC005", "A heading marker must be followed by one space."))
    return findings


def check_terms(path: Path, text: str, policy: dict) -> list[Finding]:
    findings: list[Finding] = []
    rules = [(re.compile(item["pattern"], re.IGNORECASE), item) for item in policy.get("deprecated_terms", [])]
    for number, raw in prose_lines(text):
        if "doclint: allow-terms" in raw:
            continue
        line = without_inline_code(raw)
        for pattern, item in rules:
            match = pattern.search(line)
            if match:
                findings.append(Finding(path, number, "TERM001", f"Deprecated term '{match.group(0)}'. Use {item['replacement']}. {item['reason']}"))
    return findings


def check_code_terms(path: Path, text: str, policy: dict) -> list[Finding]:
    findings: list[Finding] = []
    for number, raw in prose_lines(text):
        if raw.lstrip().startswith("#") or "doclint: allow-code-terms" in raw:
            continue
        prose = without_inline_code(raw)
        for term in policy.get("canonical_code_terms", []):
            if re.search(re.escape(term), prose, re.IGNORECASE):
                findings.append(Finding(path, number, "TERM002", f"Canonical code term '{term}' must use inline code formatting."))
    return findings


def check_links(root: Path, path: Path, text: str) -> list[Finding]:
    findings: list[Finding] = []
    pattern = re.compile(r"(?<!!)\[[^]]+\]\(([^)]+)\)")
    for number, line in prose_lines(text):
        for raw_target in pattern.findall(line):
            target = raw_target.split("#", 1)[0]
            if not target or "://" in target or target.startswith("mailto:"):
                continue
            resolved = (root / path.parent / target).resolve()
            try:
                resolved.relative_to(root.resolve())
            except ValueError:
                findings.append(Finding(path, number, "LINK001", f"Local link escapes the repository: {target}"))
                continue
            if not resolved.exists():
                findings.append(Finding(path, number, "LINK002", f"Broken local link: {target}"))
    return findings


def links_to(root: Path, path: Path, text: str, target: Path) -> bool:
    pattern = re.compile(r"(?<!!)\[[^]]+\]\(([^)]+)\)")
    expected = (root / target).resolve()
    for _, line in prose_lines(text):
        for raw_target in pattern.findall(line):
            value = raw_target.split("#", 1)[0]
            if value and "://" not in value and not value.startswith("mailto:"):
                if (root / path.parent / value).resolve() == expected:
                    return True
    return False


def check_foundation(root: Path, policy: dict) -> list[Finding]:
    findings: list[Finding] = []
    foundation = Path(policy["foundation_document"])
    if not (root / foundation).is_file():
        return [Finding(foundation, 1, "DOC007", "The protocol foundation document is missing.")]

    for value in policy.get("foundation_consumers", []):
        consumer = Path(value)
        consumer_path = root / consumer
        if not consumer_path.is_file():
            findings.append(Finding(consumer, 1, "DOC008", "A required foundation consumer is missing."))
            continue
        text = consumer_path.read_text(encoding="utf-8")
        if not links_to(root, consumer, text, foundation):
            findings.append(Finding(consumer, 1, "DOC009", f"Required foundation consumer must link to {foundation}."))
    return findings


def check_catalog(root: Path, policy: dict) -> list[Finding]:
    expected = [Path(value) for value in policy.get("ordered_documents", [])]
    if not expected:
        return []

    documents = root / "documents"
    actual = {
        path.relative_to(root)
        for path in documents.glob("*.md")
        if path.name != "README.md"
    }
    expected_set = set(expected)
    findings: list[Finding] = []

    for path in expected:
        if path not in actual:
            findings.append(Finding(path, 1, "DOC011", "A document from the canonical sequence is missing."))

    for path in sorted(actual - expected_set):
        findings.append(Finding(path, 1, "DOC012", "Document is not part of the canonical numbered sequence."))

    index_path = Path("documents/README.md")
    index_text = (root / index_path).read_text(encoding="utf-8")
    positions: list[int] = []
    for path in expected:
        marker = f"({path.name})"
        position = index_text.find(marker)
        if position == -1:
            findings.append(Finding(index_path, 1, "DOC013", f"Documentation index must link to {path.name}."))
        else:
            positions.append(position)

    if len(positions) == len(expected) and positions != sorted(positions):
        findings.append(Finding(index_path, 1, "DOC014", "Documentation index must follow the canonical numeric sequence."))
    return findings


def check_index(root: Path, policy: dict) -> list[Finding]:
    path = Path("documents/README.md")
    text = (root / path).read_text(encoding="utf-8")
    required = policy.get("required_foundation_links", [])
    findings: list[Finding] = []
    for name in required:
        if f"({name})" not in text:
            findings.append(Finding(path, 1, "DOC006", f"Documentation index must link to {name}."))

    first_link = re.search(r"\[[^]]+\]\(([^)#]+\.md)(?:#[^)]+)?\)", text)
    if required and (not first_link or first_link.group(1) != required[0]):
        findings.append(Finding(path, 1, "DOC010", f"Documentation index must begin with {required[0]}."))
    return findings


def _reject_duplicate_members(pairs: list[tuple[str, object]]) -> dict:
    value: dict = {}
    for key, item in pairs:
        if key in value:
            raise ValueError(f"duplicate JSON member: {key}")
        value[key] = item
    return value


def _reject_json_number(value: str) -> None:
    raise ValueError(f"JSON numeric token is forbidden: {value}")


def load_contract_json(path: Path) -> object:
    return json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=_reject_duplicate_members,
        parse_int=_reject_json_number,
        parse_float=_reject_json_number,
        parse_constant=_reject_json_number,
    )


def validate_contract_scalar(value: object) -> None:
    if isinstance(value, str):
        value.encode("utf-8")
        if unicodedata.normalize("NFC", value) != value:
            raise ValueError("contract strings must be NFC")
    elif value is None or isinstance(value, bool):
        return
    elif isinstance(value, list):
        for item in value:
            validate_contract_scalar(item)
    elif isinstance(value, dict):
        for key, item in value.items():
            if not key.isascii():
                raise ValueError("contract object members must be ASCII")
            validate_contract_scalar(key)
            validate_contract_scalar(item)
    else:
        raise ValueError(f"unsupported contract scalar: {type(value).__name__}")


def canonical_contract_json(value: object) -> bytes:
    validate_contract_scalar(value)
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def prefixed_sha256(domain: str, value: object) -> str:
    payload = domain.encode("ascii") + b"\x00" + canonical_contract_json(value)
    return f"sha256_{hashlib.sha256(payload).hexdigest()}"


def fixture_records(value: object) -> Iterable[dict]:
    if isinstance(value, dict):
        required = {
            "contract_version",
            "record_kind",
            "bch_id",
            "sequence",
            "previous_record_hash",
            "actor_bond_id",
            "observed_at_unix_ms",
            "body",
            "record_hash",
        }
        if required.issubset(value):
            yield value
        for item in value.values():
            yield from fixture_records(item)
    elif isinstance(value, list):
        for item in value:
            yield from fixture_records(item)


def fixture_histories(value: object) -> Iterable[list[dict]]:
    if isinstance(value, dict):
        history = value.get("history")
        if isinstance(history, list):
            yield history
        for item in value.values():
            yield from fixture_histories(item)
    elif isinstance(value, list):
        for item in value:
            yield from fixture_histories(item)


def check_core_contract(root: Path, policy: dict) -> list[Finding]:
    config = policy.get("core_contract")
    if not config:
        return []

    document = Path(config["document"])
    document_path = root / document
    if not document_path.is_file():
        return [Finding(document, 1, "CORE001", "The normative Core client contract is missing.")]

    findings: list[Finding] = []
    document_text = document_path.read_text(encoding="utf-8")
    for value in config.get("consumers", []):
        consumer = Path(value)
        consumer_path = root / consumer
        if not consumer_path.is_file() or not links_to(
            root,
            consumer,
            consumer_path.read_text(encoding="utf-8") if consumer_path.is_file() else "",
            document,
        ):
            findings.append(Finding(consumer, 1, "CORE002", f"Required consumer must link to {document}."))

    corpus = Path(config["fixture_corpus"])
    digest_path = Path(config["fixture_digest"])
    if not (root / corpus).is_file():
        findings.append(Finding(corpus, 1, "CORE003", "The canonical Core fixture corpus is missing."))
        return findings
    if not (root / digest_path).is_file():
        findings.append(Finding(digest_path, 1, "CORE004", "The canonical Core fixture digest is missing."))
        return findings

    try:
        value = load_contract_json(root / corpus)
        validate_contract_scalar(value)
    except (UnicodeError, json.JSONDecodeError, ValueError) as error:
        findings.append(Finding(corpus, 1, "CORE005", f"Invalid Core fixture corpus: {error}"))
        return findings

    required_top_level = {
        "contract_version",
        "fixture_corpus_version",
        "production_registries",
        "cases",
    }
    if not isinstance(value, dict) or set(value) != required_top_level:
        findings.append(Finding(corpus, 1, "CORE006", "Core fixture corpus must use the exact closed top-level schema."))
        return findings

    if value["contract_version"] != config["contract_version"]:
        findings.append(Finding(corpus, 1, "CORE007", "Core fixture contract version does not match policy."))
    if value["fixture_corpus_version"] != config["fixture_corpus_version"]:
        findings.append(Finding(corpus, 1, "CORE008", "Core fixture corpus version does not match policy."))

    registry_names = set(config["production_registry_names"])
    registries = value["production_registries"]
    if not isinstance(registries, dict) or set(registries) != registry_names:
        findings.append(Finding(corpus, 1, "CORE009", "Production registries must use the exact policy-defined set."))
    elif any(not isinstance(registries[name], list) or registries[name] for name in registry_names):
        findings.append(Finding(corpus, 1, "CORE010", "Phase 0 production registries must remain empty."))

    cases = value["cases"]
    case_ids: set[str] = set()
    if not isinstance(cases, list) or not cases:
        findings.append(Finding(corpus, 1, "CORE011", "Core fixture corpus must contain at least one case."))
    else:
        for case in cases:
            if not isinstance(case, dict) or set(case) != {"case_id", "input", "expected"}:
                findings.append(Finding(corpus, 1, "CORE012", "Each fixture case must use the exact closed case schema."))
                continue
            case_id = case["case_id"]
            if not isinstance(case_id, str) or not case_id or case_id in case_ids:
                findings.append(Finding(corpus, 1, "CORE013", "Fixture case identifiers must be non-empty and unique."))
            else:
                case_ids.add(case_id)
            input_value = case["input"]
            required_input = {
                "contract_version",
                "operation_id",
                "expected_state_revision",
                "command",
                "state",
                "verified_context",
            }
            if not isinstance(input_value, dict) or set(input_value) != required_input:
                findings.append(Finding(corpus, 1, "CORE020", "Fixture inputs must use the exact closed transition schema."))
                continue
            state = input_value["state"]
            expected_revision = input_value["expected_state_revision"]
            if state is None:
                revision_matches = expected_revision is None
            else:
                revision_matches = (
                    isinstance(state, dict)
                    and isinstance(state.get("state_revision"), str)
                    and expected_revision == state["state_revision"]
                )
            if not revision_matches:
                findings.append(Finding(corpus, 1, "CORE021", "Fixture expected state revision must match supplied state."))
            kind = input_value.get("command", {}).get("kind") if isinstance(input_value, dict) else None
            if not isinstance(kind, str) or not kind.startswith("fixture."):
                findings.append(Finding(corpus, 1, "CORE014", "Fixture commands must remain in the fixture namespace."))
            expected = case["expected"]
            if not isinstance(expected, dict) or set(expected) not in ({"ok"}, {"error"}):
                findings.append(Finding(corpus, 1, "CORE015", "Each fixture expectation must contain exactly ok or error."))

    for record in fixture_records(value):
        if set(record) != {
            "contract_version",
            "record_kind",
            "bch_id",
            "sequence",
            "previous_record_hash",
            "actor_bond_id",
            "observed_at_unix_ms",
            "body",
            "record_hash",
        }:
            findings.append(Finding(corpus, 1, "CORE016", "Fixture history records must use the exact closed schema."))
            continue
        unhashed = {key: item for key, item in record.items() if key != "record_hash"}
        expected_hash = prefixed_sha256("0x1:core-fixture-record:v0", unhashed)
        if record["record_hash"] != expected_hash:
            findings.append(Finding(corpus, 1, "CORE017", "Fixture history record hash is invalid."))

    for history in fixture_histories(value):
        previous_hash = None
        for index, record in enumerate(history):
            if not isinstance(record, dict) or "record_hash" not in record:
                findings.append(Finding(corpus, 1, "CORE022", "Fixture history contains a non-record value."))
                break
            if record.get("sequence") != str(index) or record.get("previous_record_hash") != previous_hash:
                findings.append(Finding(corpus, 1, "CORE023", "Fixture history is not a continuous hash-linked sequence."))
                break
            previous_hash = record["record_hash"]

    expected_digest = prefixed_sha256(config["fixture_digest_domain"], value)
    digest_bytes = (root / digest_path).read_bytes()
    if digest_bytes != f"{expected_digest}\n".encode("ascii"):
        findings.append(Finding(digest_path, 1, "CORE018", "Core fixture digest does not match canonical corpus bytes."))
    if expected_digest not in document_text:
        findings.append(Finding(document, 1, "CORE019", "Core contract must publish the validated fixture digest."))

    return findings


def run(root: Path, policy_path: Path) -> list[Finding]:
    policy = load_policy(policy_path)
    findings: list[Finding] = []
    for path in markdown_files(root, policy):
        text = (root / path).read_text(encoding="utf-8")
        findings += check_structure(path, text)
        findings += check_terms(path, text, policy)
        findings += check_code_terms(path, text, policy)
        findings += check_links(root, path, text)
    findings += check_foundation(root, policy)
    findings += check_catalog(root, policy)
    findings += check_index(root, policy)
    findings += check_core_contract(root, policy)
    return sorted(findings, key=lambda finding: (str(finding.path), finding.line, finding.code))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--policy", type=Path, default=Path(".github/documentation-style.json"))
    args = parser.parse_args()
    root = args.root.resolve()
    policy = args.policy if args.policy.is_absolute() else root / args.policy
    findings = run(root, policy)
    for finding in findings:
        print(finding.github())
    print(f"documentation lint {'failed with ' + str(len(findings)) + ' finding(s)' if findings else 'passed'}")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
