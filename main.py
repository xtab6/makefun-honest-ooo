#!/usr/bin/env python3
"""The Painfully Honest Out-of-Office — make.fun entry.

Writes one painfully honest but still polite out-of-office auto-reply to
/output/entry.txt. Stdlib only, no network, deterministic: the same bytes
on every run.

Run: python3 main.py
"""

import os
import sys

# One sentence, 167 characters: honest about being too tired to do the
# email justice, polite about answering it well next week instead.
ENTRY = (
    "I'm out of office until Monday \u2014 I took this week off because "
    "I was too tired to do your email justice, and I would rather answer "
    "it well next week than badly today."
)

MAX_CHARS = 200


def resolve_output_path() -> str:
    """Return the entry file path, honouring the harness output dir."""
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    if not out_dir:
        print("OUTPUT_DIR is empty", file=sys.stderr)
        raise ValueError("empty output directory")
    return os.path.join(out_dir, "entry.txt")


def main() -> int:
    if not 1 <= len(ENTRY) <= MAX_CHARS:
        print(
            "entry is %d characters, must be 1..%d" % (len(ENTRY), MAX_CHARS),
            file=sys.stderr,
        )
        return 1
    if not ENTRY.strip():
        print("entry is only whitespace", file=sys.stderr)
        return 1

    try:
        path = resolve_output_path()
    except ValueError:
        return 1

    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
    except OSError as exc:
        print("cannot create output dir: %s" % exc, file=sys.stderr)
        return 1

    try:
        with open(path, "w", encoding="utf-8", newline="") as handle:
            handle.write(ENTRY)
    except OSError as exc:
        print("cannot write %s: %s" % (path, exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
