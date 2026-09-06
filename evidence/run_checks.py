from __future__ import annotations

import subprocess
import sys


COMMANDS = [
    [sys.executable, "evidence/validate_claims.py"],
    [sys.executable, "evidence/redaction_check.py"],
    [
        sys.executable,
        "-m",
        "unittest",
        "discover",
        "-s",
        "evidence",
        "-t",
        ".",
        "-p",
        "test_*.py",
    ],
]


def main() -> int:
    for command in COMMANDS:
        result = subprocess.run(command, check=False)
        if result.returncode:
            return result.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
