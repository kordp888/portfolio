from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
TEXT_SUFFIXES = {".md", ".json", ".py", ".txt", ".yml", ".yaml"}
PATTERNS = {
    "local_absolute_path": re.compile(r"(?:/Users/|/home/|[A-Za-z]:\\\\Users\\\\)"),
    "email": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
    "phone": re.compile(r"(?<!\d)01[016789][ -]?\d{3,4}[ -]?\d{4}(?!\d)"),
    "ipv4": re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
    "token": re.compile(r"(?:github_pat_|ghp_|AIza|sk-)[A-Za-z0-9_-]{8,}"),
    "url_query": re.compile(r"https?://[^\s)]+\?[^\s)]"),
}


def scan() -> list[str]:
    findings = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if path.name == Path(__file__).name:
            continue
        text = path.read_text(encoding="utf-8")
        for label, pattern in PATTERNS.items():
            if pattern.search(text):
                findings.append(f"{path.relative_to(ROOT)}: {label}")
    return findings


def main() -> int:
    findings = scan()
    if findings:
        print("\n".join(findings))
        return 1
    print("redaction: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
