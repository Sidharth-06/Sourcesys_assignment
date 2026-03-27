"""Check whether a string is a palindrome."""

from __future__ import annotations

import argparse
import re


def normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9]", "", text.lower())


def is_palindrome(text: str) -> bool:
    cleaned = normalize(text)
    return cleaned == cleaned[::-1]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Detect palindromes in text.")
    parser.add_argument("text", help="Text to check")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    result = is_palindrome(args.text)
    verdict = "is" if result else "is not"
    print(f"{args.text!r} {verdict} a palindrome")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
