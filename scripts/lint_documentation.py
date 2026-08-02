#!/usr/bin/env python3
"""Validate 0x1 documentation structure, links, style, and terminology."""

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
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def markdown_files(root: Path, policy: dict) -> list[Path]:
    excluded = {Path(value) for value in policy.get("excluded_paths", [])}
    result: set[Path] = set()
    for configured in policy["roots"]:
        candidate = root / configured
        if candidate.is_file() and candidate.suffix == ".md":
            result.add(candidate.relative_to(root))
        elif candidate.is_dir():
            result.update(path.relative_to(root) for path in candidate.rglob("*.md"))
    return sorted(path for path in result if path not in excluded)


def prose_lines(text: str) -> Iterable[tuple[int, str]]:
    in_fence = False
    fence = ""
    for number, line in enumerate(text.splitlines(), start=1):
        stripped = line.lstrip()
        match = re.match(r"(```+|~~~+)", stripped)
        if match:
            marker = match.group(1)[0]
            if not in_fence:
                in_fence = True
                fence = marker
            elif marker == fence:
                in_fence = False
                fence = ""
            continue
        if not in_fence:
            yield number, line


def strip_inline_code(line: str) -> str:
    return re.sub(r"`[^`]*`", "", line)


def check_structure(path: Path, text: str) -> list[Finding]:
    findings: list[Finding] = []
    lines = text.splitlines()
    headings = [(i, line) for i, line in enumerate(lines, start=1) if line.startswith("# ")]
    if len(headings) != 1:
        findings.append(Finding(path, 1, "DOC001", "Markdown documents must contain exactly one H1 heading."))
    elif headings[0][0] != 1:
        findings.append(Finding(path, headings[0][0], "DOC002", "The H1 heading must be the first line."))
    for number, line in enumerate(lines, start=1):
        if line.rstrip() != line:
            findings.append(Finding(path, number, "DOC003", "Trailing whitespace is not allowed."))
        if "\t" in line:
            findings.append(Finding(path, number, "DOC004", "Tabs are not allowed in Markdown."))
        if re.match(r"^#{1,6}[^ #]", line):
            findings.append(Finding(path, number, "DOC005", "A heading marker must be followed by one space."))
    return findings


def check_terms(path: Path, text: str, policy: dict) -> list[Finding]:
    findings: list[Finding] = []
    compiled = [
        (re.compile(item["pattern"], re.IGNORECASE), item)
        for item in policy.get("deprecated_terms", [])
    ]
    for number, raw_line in prose_lines(text):
        if "doclint: allow-terms" in raw_line:
            continue
        line = strip_inline_code(raw_line)
        for pattern, item in compiled:
            match = pattern.search(line)
            if match:
                findings.append(
                    Finding(
                        path,
                        number,
                        "TERM001",
                        f"Deprecated term '{match.group(0)}'. Use {item['replacement']}. {item['reason']}",
                    )
                )
    return findings


def check_code_terms(path: Path, text: str, policy: dict) -> list[Finding]:
    findings: list[Finding] = []
    for number, raw_line in prose_lines(text):
        if raw_line.lstrip().startswith("#"):
            continue
        for term in policy.get("canonical_code_terms", []):
            for match in re.finditer(re.escape(term), raw_line, re.IGNORECASE):
                start, end = match.span()
                before = raw_line[:start]
                after = raw_line[end:]
                if before.count("`") % 2 == 1 and after.count("`") % 2 == 1:
                    continue
                findings.append(Finding(path, number, "TERM002", f"Canonical code term '{term}' must use inline code formatting."))
                break
    return findings


def check_links(root: Path, path: Path, text: str) -> list[Finding]:
    findings: list[Finding] = []
    link_pattern = re.compile(r"(?<!!)\[[^]]+\]\(([^)]+)\)")
    for number, line in prose_lines(text):
        for target in link_pattern.findall(line):
            target = target.split("#", 1)[0]
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


def check_index(root: Path, policy: dict) -> list[Finding]:
    path = Path("documents/README.md")
    text = (root / path).read_text(encoding="utf-8")
    findings: list[Finding] = []
    for required in policy.get("required_foundation_links", []):
        if f"({required})" not in text:
            findings.append(Finding(path, 1, "DOC006", f"Documentation index must link to {required}."))
    return findings


def run(root: Path, policy_path: Path) -> list[Finding]:
    policy = load_policy(policy_path)
    findings: list[Finding] = []
    for relative in markdown_files(root, policy):
        text = (root / relative).read_text(encoding="utf-8")
        findings.extend(check_structure(relative, text))
        findings.extend(check_terms(relative, text, policy))
        findings.extend(check_code_terms(relative, text, policy))
        findings.extend(check_links(root, relative, text))
    findings.extend(check_index(root, policy))
    return sorted(findings, key=lambda item: (str(item.path), item.line, item.code))


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
    if findings:
        print(f"documentation lint failed with {len(findings)} finding(s)")
        return 1
    print("documentation lint passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
