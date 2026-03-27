"""Count words, characters, and lines in a text file or plain input."""

from __future__ import annotations

import argparse
from pathlib import Path


def analyze_text(text: str) -> dict[str, int]:
    words = text.split()
    return {
        "lines": len(text.splitlines()) if text else 0,
        "words": len(words),
        "characters": len(text),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Report basic text statistics.")
    parser.add_argument("input", help="Text to analyze or a path to a text file")
    return parser


def load_input(value: str) -> str:
    path = Path(value)
    if path.is_file():
        return path.read_text(encoding="utf-8")
    return value


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    text = load_input(args.input)
    stats = analyze_text(text)
    print(f"Lines: {stats['lines']}")
    print(f"Words: {stats['words']}")
    print(f"Characters: {stats['characters']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
