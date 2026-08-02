#!/usr/bin/env python3
"""Validate 0x1 documentation structure, foundation, links, style, and terminology."""

from __future__ import annotations

import argparse
import json
import re
import sys
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
